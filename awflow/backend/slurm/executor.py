r"""
Definition of the Slurm executor.
"""

import cloudpickle as pickle
import os
import tempfile

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG


def execute(workflow: DAWG, base: str = '.workflows', **kwargs) -> None:
    os.mkdir(base, exist_ok=True)  # Create the base directory
    directory = tempfile.mkdtemp(dir=base)
    raise NotImplementedError
