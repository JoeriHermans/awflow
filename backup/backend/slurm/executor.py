r"""
Definition of the Slurm executor.
"""

import os
import tempfile
import awflow.plugins as plugins

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node
from awflow.utils.executor import generate_executables



BACKEND = 'slurm'



def execute(workflow: DAWG, dir: str = '.workflows', **kwargs) -> None:
    # Preparing the execution files.
    os.makedirs(dir, exist_ok=True)  # Create the base directory
    directory = tempfile.mkdtemp(dir=dir)
    plugins.apply_defaults(backend=BACKEND, workflow=workflow, **kwargs)
    # Generate the executables for the graph.
    generate_executables(workflow=workflow, dir=directory)
    # Process Slurm attributes
    add_default_attributes(workflow=workflow)
    translate_attributes(workflow=workflow)
    # Set the partition of the Slurm jobs.

    raise NotImplementedError


def add_default_attributes(workflow: DAWG) -> None:
    for node in workflow.nodes:
        # Check if a slurm environment already exists.
        if BACKEND not in node.attributes.keys():
            node[BACKEND] = {}
        # Set default attributes
        node[BACKEND]['--chdir='] = node['chdir']
        node[BACKEND]['--export='] = 'ALL'
        node[BACKEND]['--job-name='] = node.name
        node[BACKEND]['--parsable'] = ''
        node[BACKEND]['--requeue'] = ''
        # Prepare the logging directory
        fmt = 'logging/' + node.name
        if node.tasks > 1:
            fmt += '-%A_%a.log'
        else:
            fmt += '-%j.log'
        node[BACKEND]['--output='] = fmt


def translate_attributes(workflow: DAWG) -> None:
    for node in workflow.nodes:
        translate_attribute_cpu(node)
        translate_attribute_gpu(node)
        translate_attribute_memory(node)
        translate_attribute_timelimit(node)


def translate_attribute_cpu(node: Node) -> None:
    if 'cpus' in node.attributes.keys():
        node[BACKEND]['--cpus-per-task='] = str(node['cpus'])


def translate_attribute_gpu(node: Node) -> None:
    if 'gpus' in node.attributes.keys():
        node[BACKEND]['--gres=gpu:'] = str(node['gpus'])


def translate_attribute_memory(node: Node) -> None:
    if 'memory' in node.attributes.keys():
        node[BACKEND]['--mem='] = node['memory']


def translate_attribute_timelimit(node: Node) -> None:
    if 'timelimit' in node.attributes.keys():
        node[BACKEND]['--time='] = node['timelimit']
