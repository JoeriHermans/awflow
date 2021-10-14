import awflow

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node

from typing import List



def apply_defaults(node: Node, **kwargs) -> None:
    # Only apply to Slurm backend
    if awflow.backend.__backend__ != 'slurm':
        return
    partition = kwargs.get('partition', None)
    if partition is not None:
        if not isinstance(partition, list):
            partition = [partition]
        set_partitions(node, partition)


def set_partitions(node: Node, partitions: List[str]) -> None:
    if '--partition=' not in node.attributes.keys():
        node['--partition='] = ','.join(partitions)


def generate_before(node: Node) -> List[str]:
    return []


def generate_after(node: Node) -> List[str]:
    return []
