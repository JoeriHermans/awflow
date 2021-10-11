r"""
Utilities that are specific to *currently* allocated backend.
"""

import cloudpickle as pickle
import importlib
import os

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node
from awflow.utils.backend import autodetect
from awflow.utils.backend import available_backends

from types import ModuleType
from typing import Optional
from typing import Union



def execute(workflow: Optional[DAWG] = None, backend: str = autodetect(), **kwargs) -> None:
    # Verify the specified backend.
    # TODO Do not forget to uncomment.
    # backends = available_backends()
    # if backend not in backends:
    #    raise ValueError('`' + backend + '` is not available! Available: ' + str(backends))

    import awflow
    if workflow is None:
        workflow = awflow.workflow  # Use default workflow
    module = importlib.import_module('awflow.backend.' + backend)
    executor = getattr(module, 'execute')
    executor(workflow, **kwargs)


def executable_name(node: Node) -> str:
    return str(node.identifier) + '.code'


def generate_executables(workflow: DAWG, dir: str) -> None:
    cwd = os.getcwd()
    os.chdir(dir)
    for node in workflow.nodes:
        subroutine = pickle.dumps(node.f)
        with open(executable_name(node), 'wb') as f:
            f.write(subroutine)
    os.chdir(cwd)
