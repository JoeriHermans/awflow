import os

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node

from typing import List



def apply_defaults(node: Node, **kwargs) -> None:
    if 'conda' not in node.attributes.keys():
        environment = kwargs.get('conda', None)
        if environment is None:
            if 'CONDA_DEFAULT_ENV' in os.environ:
                environment = os.environ['CONDA_DEFAULT_ENV']
                set_environment(node, environment)
        else:
            set_environment(node, environment)


def set_environment(node: Node, environment: str) -> None:
    if 'conda' not in node.attributes.keys():
        node['conda'] = environment


def generate_before(node: Node) -> List[str]:
    if 'conda' in node.attributes.keys():
        return ['eval "$(conda shell.bash hook)"', 'conda activate ' + node['conda']]
    else:
        return []


def generate_after(node: Node) -> List[str]:
    return []
