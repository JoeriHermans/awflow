r"""
Decorators specific to the Slurm partition plugin.
"""

from awflow.node import Node
from awflow.plugins.partition import set_partitions
from awflow.utils.dawg import add_and_get_node
from awflow.utils.decorator import parameterized
from awflow.utils.generic import is_iterable

from typing import List
from typing import Callable
from typing import Union



@parameterized
def partition(f: Callable, partition: Union[str, List[str]]) -> Callable:
    node = add_and_get_node(f)
    if not is_iterable(partition):
        partition = [partition]
    set_partitions(node, partition)

    return f
