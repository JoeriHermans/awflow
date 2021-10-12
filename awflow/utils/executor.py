r"""
Utilities that are specific to the executors of backends.
"""

import cloudpickle as pickle
import os

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node



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
