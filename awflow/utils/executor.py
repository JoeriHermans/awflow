r"""
Utilities that are specific to *currently* allocated backend.
"""

import importlib

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.utils.backend import autodetect
from awflow.utils.backend import available_backends

from types import ModuleType
from typing import Optional
from typing import Union



def execute(workflow: Optional[DAWG] = None, backend: str = autodetect(), **kwargs) -> None:
    # Verify the specified backend.
    backends = available_backends()
    if backend not in backends:
        raise ValueError('`' + backend + '` is not available! Available: ' + str(backends))

    import awflow
    if workflow is None:
        workflow = awflow.workflow  # Use default workflow
    module = importlib.import_module('awflow.backend.' + backend)
    executor = getattr(module, 'execute')
    executor(workflow, **kwargs)
