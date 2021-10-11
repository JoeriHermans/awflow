r"""
Decorators for the `chdir` plugin.
"""

from awflow.node import Node
from awflow.plugins.chdir import set_working_directory
from awflow.utils.dawg import add_and_get_node
from awflow.utils.decorator import parameterized

from typing import Callable



@parameterized
def chdir(f: Callable, dir: str) -> Callable:
    node = add_and_get_node(f)
    set_working_directory(node, dir)

    return f
