r"""
Generic decorators for workflow nodes.
"""

from __future__ import annotations

import awflow

from awflow.node import Node
from awflow.utils.decorator import parameterized
from awflow.utils.generic import is_iterable
from awflow.utils.dawg import add_and_get_node

from typing import Callable
from typing import Union



def disable(f: Callable) -> Callable:
    node = add_and_get_node(f)
    node.prunable = True

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


@parameterized
def cpus(f: Callable, n: int) -> Callable:
    node = add_and_get_node(f)
    awflow.backend.cpus(node, n)

    return f


@parameterized
def cpus_and_memory(f: Callable, n: int, memory: str) -> Callable:
    node = add_and_get_node(f)
    awflow.backend.cpus(node, n)
    awflow.backend.memory(node, memory)

    return f


@parameterized
def gpus(f: Callable, n: int) -> Callable:
    node = add_and_get_node(f)
    awflow.backend.gpus(node, n)

    return f


@parameterized
def memory(f: Callable, memory: str) -> Callable:
    node = add_and_get_node(f)
    awflow.backend.memory(node, memory)

    return f


@parameterized
def timelimit(f: Callable, timelimit: str) -> Callable:
    node = add_and_get_node(f)
    awflow.backend.timelimit(node, timelimit)

    return f


@parameterized
def postcondition(f: Callable, condition: Callable) -> Callable:
    node = add_and_get_node(f)
    node.add_postcondition(condition)

    return f
