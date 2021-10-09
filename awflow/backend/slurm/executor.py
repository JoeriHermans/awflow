r"""
Definition of the Slurm executor.
"""

import os
import tempfile

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node
from awflow.utils.executor import generate_executables


def execute(workflow: DAWG, dir: str = '.workflows', **kwargs) -> None:
    # Preparing the execution files.
    os.makedirs(base, exist_ok=True)  # Create the base directory
    directory = tempfile.mkdtemp(dir=base)
    # Generate the executables for the graph.
    generate_executables(workflow=workflow, directory=directory)

    raise NotImplementedError
