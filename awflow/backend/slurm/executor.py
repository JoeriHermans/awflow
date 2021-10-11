r"""
Definition of the Slurm executor.
"""

import os
import tempfile

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node
from awflow.utils.executor import generate_executables



BACKEND = 'slurm'



def execute(workflow: DAWG, dir: str = '.workflows', **kwargs) -> None:
    # Preparing the execution files.
    os.makedirs(dir, exist_ok=True)  # Create the base directory
    directory = tempfile.mkdtemp(dir=dir)
    # Generate the executables for the graph.
    generate_executables(workflow=workflow, dir=directory)
    # Process Slurm attributes
    add_default_attributes(workflow=workflow, cwd=cwd)
    set_logging_directory(workflow=workflow, dir=directory)
    translate_attributes(workflow=workflow)

    raise NotImplementedError


def add_default_attributes(workflow: DAWG) -> None:
    for node in workflow.nodes:
        # Check if a slurm environment already exists.
        if BACKEND not in node.attributes.keys():
            node[BACKEND] = {}
        # Set default attributes
        node[BACKEND]['--export'] = 'ALL'  # Exports all environment variables
        node[BACKEND]['--parsable'] = ''   # Enables convienient parsing of task ID
        node[BACKEND]['--requeue'] = ''    # Automatically requeue on failure
        node[BACKEND]['--chdir'] = os.getcwd()
        # Prepare the logging directory
        fmt = 'logging/' + node.name
        if node.tasks > 1:
            fmt += '-%A_%a.log'
        else:
            fmt += '-%j.log'
        node[BACKEND]['--output'] = fmt


def translate_attributes(workflow: DAWG) -> None:
    pass
