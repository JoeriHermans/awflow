from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node


def set_environment(node: Node, environment: str) -> None:
    if 'conda' not in node.attributes.keys():
        node['conda'] = environment


def generate_activate(node: Node) -> list[str]:
    if 'conda' in node.attributes.keys():
        return ['eval "$(conda shell.bash hook)"', 'conda activate ' + node['conda']]
    else:
        return []
