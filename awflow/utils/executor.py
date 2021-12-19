r"""
Utilities that are specific to the executors of backends.
"""

import cloudpickle as pickle
import json
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


def generate_metadata(workflow: DAWG, dir: str) -> None:
    cwd = os.getcwd()
    os.chdir(dir)
    data = json.dumps(workflow.metadata)
    with open('metadata.json', 'w') as f:
        f.write(data)
    os.chdir(cwd)


def generate_postconditions(workflow: DAWG, dir: str) -> None:
    cwd = os.getcwd()
    os.chdir(dir)
    postconditions = list(workflow.postconditions)
    if len(postconditions) > 0:
        with open('postconditions', 'wb') as f:
            f.write(pickle.dumps(postconditions))
    os.chdir(cwd)
