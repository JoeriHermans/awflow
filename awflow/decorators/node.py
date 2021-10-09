r"""
Generic decorators for workflow nodes.
"""

from __future__ import annotations

import awflow
import awflow.plugins as plugins

from awflow.node import Node
from awflow.utils.decorator import parameterized
from awflow.utils.generic import is_iterable
from awflow.utils.dawg import add_and_get_node

from typing import Callable
from typing import Union



@parameterized
def conda(f: Callable, environment: str) -> Callable:
    node = add_and_get_node(f)
    plugins.conda.set_environment(node, environment)

    return f


@parameterized
def dependency(f: Callable, dependencies: Union[list[Node], Node]) -> Callable:
    # Check if the dependency is a list of dependencies.
    if not is_iterable(dependencies):
        dependencies = [dependencies]
    node = add_and_get_node(f)
    for dependency in dependencies:
        if f == dependency:
            raise ValueError("A function cannot depend on itself.")
        dependency_node = add_and_get_node(dependency)
        node.add_dependency(dependency_node)

    return f


@parameterized
def name(f: Callable, name: str) -> Callable:
    node = add_and_get_node(f)
    node.name = name

    return f


@parameterized
def tasks(f: Callable, n: int) -> Callable:
    node = add_and_get_node(f)
    node.tasks = n

    return f
