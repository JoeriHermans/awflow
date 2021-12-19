import argparse
import awflow
import cloudpickle as pickle
import json
import os
import rich
import subprocess
import sys
import time

from awflow.bin.cli.utils import print_error
from rich import box
from rich.console import Console
from rich.table import Table



def main() -> None:
    module, unknown_args, args = _parse_arguments()
    module_handlers = {
        'cancel': _module_cancel,
        'clear': _module_clear,
        'list': _module_list,
        'remove': _module_remove}
    if module not in module_handlers.keys():
        raise ValueError('Module `{mod}` is unknow, execute `awflow -h`.'.format(
            mod=module))
    module_handlers[module](unknown_args, args)


def _module_cancel(unknown_args, args):
    if not awflow.backends.utils.slurm_detected():
        print_error('You can only cancel workflows running on a Slurm cluster.')
        sys.exit(1)
    ## TODO Implement


def _module_clear(unknown_args, args):
    root = os.path.abspath(args.pipeline + '/.workflows')
    if os.path.exists(root):
        workflow_directories = [os.path.abspath(f) for f in os.listdir(root) if os.path.isdir(f)]
    else:
        workflow_directories = []
    # TODO Implement


def _module_list(unknown_args, args):
    root = os.path.abspath(args.pipeline + '/.workflows')
    if os.path.exists(root):
        workflow_directories = [os.path.abspath(root + '/' + f) for f in os.listdir(root) if os.path.isdir(root + '/' + f)]
    else:
        workflow_directories = []
    # Check if workflows are available.
    if len(workflow_directories) == 0:
        print_error('[bold red]No workflows found!')
        sys.exit(1)
    # Iterate over the workflows.
    workflow_directories.sort(key=os.path.getctime, reverse=True)
    console = Console()
    table = Table(header_style='bold magenta', box=box.SIMPLE, expand=True)
    table.add_column('Progress')
    table.add_column('Status')
    table.add_column('Backend')
    table.add_column('Name')
    table.add_column('Location')
    with console.status("[blue]Checking workflows...") as status:
        for workflow in workflow_directories:
            # Check if a Slurm backend was used.
            slurm_backend = os.path.exists(workflow + '/job_identifiers')
            if slurm_backend:
                backend = 'Slurm'
            else:
                backend = 'Standalone'
            # Load the metadata of the workflow
            with open(workflow + '/metadata.json', 'r') as f:
                metadata = json.loads(f.read())
            # Load the workflows postconditions
            with open(workflow + '/postconditions', 'rb') as f:
                postconditions = [f() for f in pickle.loads(f.read())]
            completed = sum(postconditions) == len(postconditions)
            progress = str(int(sum(postconditions) / len(postconditions) * 100)) + '%'
            if completed:
                progress = '[bold green]' + progress
            else:
                progress = '[blue]' + progress
            # Determine the status of the workflow.
            status = '[blue]In progress'
            if slurm_backend:
                with open(workflow + '/job_identifiers', 'r') as f:
                    data = f.read().split('\n')
                    job_identifiers = [j for j in data if len(j) > 0]
                states = []
                for identifier in job_identifiers:
                    command = 'sacct -X -n -j {id} --format=State'.format(id=identifier)
                    outputs = subprocess.check_output(command, shell=True, text=True).split('\n')
                    states.extend([o.strip() for o in outputs if len(o.strip()) > 0])
                states = set(states)
                failed = 'FAILED' in states
                if failed:
                    status = '[bold red]Failed'
                elif len(states) == 1 and 'COMPLETED' in states:
                    status = '[bold green]Completed'
            elif completed:
                status = '[bold green]Completed'
            table.add_row(progress, status, backend, metadata['name'], workflow)
    console.print(table)


def _module_remove(unknown_args, args):
    pass  # TODO Implement


def _parse_arguments():
    parser = argparse.ArgumentParser(
        prog='awflow',
        description='Manage reproducable workflows with ease.',
        epilog='For help or bugreports please refer to ' + awflow.__github__)
    # Specify the custom arguments
    parser.add_argument('--pipeline', type=str, default='.', help='Specify directory of the pipeline (default: current directory).')

    # Verify
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # Parse the program arguments
    arguments, unknown_arguments = parser.parse_known_args()
    module = unknown_arguments[0]
    del unknown_arguments[0]

    return module, unknown_arguments, arguments
