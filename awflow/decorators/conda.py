r"""
Decorators specific to the Anaconda plugin.
"""

from awflow.node import Node
from awflow.plugins.conda import set_environment
from awflow.utils.dawg import add_and_get_node
from awflow.utils.decorator import parameterized

from typing import Callable



@parameterized
def conda(f: Callable, environment: str) -> Callable:
    node = add_and_get_node(f)
    set_environment(node, environment)

    return f
