import argparse
import awflow
import cloudpickle as pickle
import glob
import json
import os
import re
import rich
import shutil
import subprocess
import sys
import time

from awflow.bin.cli.utils import print_error
from rich import box
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table


class WorkflowState:
    CANCELLED = 0
    COMPLETED = 1
    FAILED = 2
    PENDING = 3
    RUNNING = 4
    SUSPENDED = 5


def main() -> None:
    module, unknown_args, args = _parse_arguments()
    module_handlers = {
        'cancel': _module_cancel,
        'clear': _module_clear,
        'list': _module_list}
    if module not in module_handlers.keys():
        raise ValueError('Module `{mod}` is unknow, execute `awflow -h`.'.format(
            mod=module))
    module_handlers[module](unknown_args, args)


def _module_cancel(unknown_args, args):
    if not awflow.backends.utils.slurm_detected():
       print_error('You can only cancel workflows running on a Slurm cluster.')
       sys.exit(1)
    if len(unknown_args) == 0:
        print_error('Specify the name or location of the workflow to be cancelled.')
        sys.exit(0)
    query = unknown_args[0]
    to_cancel = []
    root = os.path.abspath(args.pipeline + '/.workflows')
    to_cancel = glob.glob(root + '/*' + query + '*')
    if os.path.exists(root):
        workflow_directories = [os.path.abspath(root + '/' + f) for f in os.listdir(root) if os.path.isdir(root + '/' + f)]
    else:
        workflow_directories = []
    # Check whether a workflow name matches.
    m = re.compile('(.' + query + ')')
    for workflow in workflow_directories:
        with open(workflow + '/metadata.json') as f:
            name = json.loads(f.read())['name']
        if m.search(name):
            to_cancel.append(workflow)
    # Iterate through the to-cancel workflows:
    console = Console()
    for workflow in to_cancel:
        slurm_backend = os.path.exists(workflow + '/job_identifiers')
        if not slurm_backend:
            continue  # Can only cancel Slurm workflows
        # Check if we need to ask for permission.
        if not args.y:
            progress, status, backend, name = _fancy_workflow_state(workflow)
            table = Table(header_style='bold magenta', box=box.SIMPLE, expand=True)
            table.add_column('Postconditions')
            table.add_column('Status')
            table.add_column('Backend')
            table.add_column('Name')
            table.add_column('Location')
            progress, status, backend, name = _fancy_workflow_state(workflow)
            table.add_row(progress, status, backend, name, workflow)
            console.print(table)
            cancel = Confirm.ask('Would you like to cancel this workflow?', default=False)
            if not cancel:
                continue
        # Cancel the workflow
        _cancel_workflow(workflow)


def _module_clear(unknown_args, args):
    root = os.path.abspath(args.pipeline + '/.workflows')
    if os.path.exists(root):
        workflow_directories = [os.path.abspath(root + '/' + f) for f in os.listdir(root) if os.path.isdir(root + '/' + f)]
    else:
        workflow_directories = []
    # Remove the workflows whose postconditions have been satisified.
    console = Console()
    with console.status("[blue]Clearing workflows...") as status:
        for workflow in workflow_directories:
            state = _workflow_state(workflow)
            if status == WorkflowState.PENDING or status == WorkflowState.RUNNING:
                continue
            _cancel_workflow(workflow)
            shutil.rmtree(workflow)


def _module_list(unknown_args, args):
    root = os.path.abspath(args.pipeline + '/.workflows')
    if os.path.exists(root):
        workflow_directories = [os.path.abspath(root + '/' + f) for f in os.listdir(root) if os.path.isdir(root + '/' + f)]
    else:
        workflow_directories = []
    # Check if workflows are available.
    if len(workflow_directories) == 0:
        print_error('[bold red]No executed workflows found!')
        sys.exit(1)
    # Iterate over the workflows.
    workflow_directories.sort(key=os.path.getctime, reverse=True)
    console = Console()
    table = Table(header_style='bold magenta', box=box.SIMPLE, expand=True)
    table.add_column('Postconditions')
    table.add_column('Status')
    table.add_column('Backend')
    table.add_column('Name')
    table.add_column('Location')
    with console.status("[blue]Checking workflows...") as status:
        for workflow in workflow_directories:
            progress, status, backend, name = _fancy_workflow_state(workflow)
            table.add_row(progress, status, backend, name, workflow)
    console.print(table)


def _fancy_workflow_state(path):
    state = _workflow_state(path)
    # Set the progress.
    progress = state['progress']
    if state['completed']:
        progress = '[bold green]' + progress
    else:
        progress = '[blue]' + progress
    # Set the workflow status
    status = state['status']
    if status == WorkflowState.RUNNING:
        status = '[blue]Running'
    elif status == WorkflowState.PENDING:
        status = '[blue]Pending'
    elif status == WorkflowState.FAILED:
        status = '[bold red]Failed'
    elif status == WorkflowState.CANCELLED:
        status = '[bold red]Cancelled'
    elif status == WorkflowState.COMPLETED:
        status = '[bold green]Completed'
    elif status == WorkflowState.SUSPENDED:
        status = '[bold orange]Suspended'
    # Fetch workflow metadata
    backend = state['backend']
    name = state['name']

    return progress, status, backend, name


def _workflow_state(path):
    state = {}

    # Check if a Slurm backend was used.
    slurm_backend = os.path.exists(path + '/job_identifiers')
    if slurm_backend:
        backend = 'Slurm'
    else:
        backend = 'Standalone'
    state['backend'] = backend

    # Load the metadata of the workflow
    with open(path + '/metadata.json', 'r') as f:
        metadata = json.loads(f.read())
    # Load the workflows postconditions
    with open(path + '/postconditions', 'rb') as f:
        postconditions = [f() for f in pickle.loads(f.read())]
        completed = sum(postconditions) == len(postconditions)
        progress = str(int(sum(postconditions) / len(postconditions) * 100)) + '%'
    state['completed'] = completed
    state['metadata'] = metadata
    state['name'] = metadata['name']
    state['progress'] = progress

    # Determine the status of the workflow.
    status = WorkflowState.PENDING
    if slurm_backend:
        with open(path + '/job_identifiers', 'r') as f:
            data = f.read().split('\n')
            job_identifiers = [j for j in data if len(j) > 0]
        states = []
        for identifier in job_identifiers:
            command = 'sacct -X -n -j {id} --format=State%100'.format(id=identifier)
            outputs = subprocess.check_output(command, shell=True, text=True).split('\n')
            states.extend([o.strip().split(' ')[0] for o in outputs if len(o.strip()) > 0])
        states = set(states)
        if 'FAILED' in states:
            status = WorkflowState.FAILED
        elif 'CANCELLED' in states:
            status = WorkflowState.CANCELLED
        elif 'SUSPENDED' in states:
            status = WorkflowState.SUSPENDED
        elif 'RUNNING' in states:
            status = WorkflowState.RUNNING
        elif len(states) == 1 and 'COMPLETED' in states:
            status = WorkflowState.COMPLETED
    elif completed:
         status = WorkflowState.COMPLETED
    state['status'] = status

    return state


def _cancel_workflow(path):
    try:
        with open(path + '/job_identifiers', 'r') as f:
            data = f.read().split('\n')
            job_identifiers = [j for j in data if len(j) > 0]
        states = []
        for identifier in job_identifiers:
            command = 'scancel {id}'.format(id=identifier)
            os.system(command)
        success = True
    except:
        success = False

    return success


def _parse_arguments():
    parser = argparse.ArgumentParser(
        prog='awflow',
        description='Manage reproducable workflows with ease.',
        epilog='For help or bugreports please refer to ' + awflow.__github__)
    # Specify the custom arguments
    parser.add_argument('--pipeline', type=str, default='.', help='Specify directory of the pipeline (default: current directory).')
    parser.add_argument('-y', action='store_true', help='Perform the action without asking for permission (default: false).')

    # Verify
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # Parse the program arguments
    arguments, unknown_arguments = parser.parse_known_args()
    module = unknown_arguments[0]
    del unknown_arguments[0]

    return module, unknown_arguments, arguments
