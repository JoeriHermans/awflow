r"""
Decorators specific to the Anaconda plugin.
"""

from awflow.node import Node
from awflow.utils.decorator import parameterized
from awflow.utils.dawg import add_and_get_node

from typing import Callable



@parameterized
def conda(f: Callable, environment: str) -> Callable:
    node = add_and_get_node(f)
    plugins.conda.set_environment(node, environment)

    return f
