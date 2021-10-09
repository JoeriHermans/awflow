r"""
Utilities that are specific to *currently* allocated backend.
"""

import awflow.backend.slurm as slurm
import awflow.backend.standalone as standalone

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.utils.backend import autodetect

from types import ModuleType
from typing import Union



def execute(workflow: DAWG = None, backend: ModuleType = autodetect()) -> None:
    import awflow
    if workflow is None:
        workflow = awflow.workflow  # Use default workflow

    print(workflow)

    raise NotImplementedError
