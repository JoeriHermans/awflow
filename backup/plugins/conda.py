import os

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node



def apply_defaults(backend: str, node: Node, **kwargs) -> None:
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


def generate_before(backend: str, node: Node) -> list[str]:
    if 'conda' in node.attributes.keys():
        return ['eval "$(conda shell.bash hook)"', 'conda activate ' + node['conda']]
    else:
        return []


def generate_after(backend: str, node: Node) -> list[str]:
    return []
