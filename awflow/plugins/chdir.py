import os

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node

from typing import List



def apply_defaults(node: Node, **kwargs) -> None:
    if 'chdir' not in node.attributes.keys():
        cwd = kwargs.get('chdir', os.getcwd())
        set_working_directory(node, cwd)


def set_working_directory(node: Node, dir: str) -> None:
    if not os.path.isdir(dir):
        raise Exception('`' + dir + '` cannot be your working directory.')
    node['chdir'] = dir


def generate_before(node: Node) -> List[str]:
    if 'chdir' in node.attributes.keys():
        return ['cd ' + node['chdir']]
    else:
        return []


def generate_after(node: Node) -> List[str]:
    return []
