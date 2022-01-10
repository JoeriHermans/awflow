r"""Workflow graph components."""

import inspect

from functools import cached_property
from typing import Any, Callable, Dict, Iterator, List, Set, Tuple, Union



class Node:
    r"""Abstract graph node."""

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self._children = {}
        self._parents = {}

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return repr(self)

    def add_child(self, node: 'Node', edge: Any = None) -> None:
        self._children[node] = edge
        node._parents[self] = edge

    def add_parent(self, node: 'Node', edge: Any = None) -> None:
        node.add_child(self, edge)

    def rm_child(self, node: 'Node') -> None:
        if node in self._children:
            del self._children[node]
        if self in node._parents:
            del node._parents[self]

    def rm_parent(self, node: 'Node') -> None:
        node.rm_child(self)

    @property
    def children(self) -> List['Node']:
        return list(self._children)

    @property
    def parents(self) -> List['Node']:
        return list(self._parents)



class Job(Node):
    r"""Node in compute graph representing an executable job."""

    def __init__(
        self,
        fn: Callable,
        name: str = None,
        array: Union[int, Set[int], range] = None,
        **kwargs,
    ):
        super().__init__(fn.__name__ if name is None else name)
        # Prepare job properties and their defaults
        self._fn = fn
        self.settings = {}
        self.settings.update(kwargs)
        if type(array) is int:
            array = range(array)
        self.array = array
        # Dependency behaviour
        self._waitfor = 'all'
        # Postconditions.
        self.postconditions = []
        self.pruned = False
        self.disabled = False

    def _verify_postconditions(self, args: Any = None) -> bool:
        if len(self.postconditions) > 0:
            verified = True
            for postcondition in self.postconditions:
                sig = inspect.signature(postcondition)
                if len(sig.parameters) >= 1:
                    verified &= postcondition(args)
                else:
                    verified &= postcondition()
        else:
            verified = True

        return verified

    @property
    def fn(self) -> Callable:
        name, f = self.name, self._fn

        def call(*args) -> Any:
            result = f(*args)

            assert self._verify_postconditions(*args), f'job {name} does not satisfy its postcondition'

            return result

        return call

    def __call__(self, *args) -> Any:
        return self.fn(*args)

    @property
    def dependencies(self) -> Dict['Job', str]:
        return self._parents

    def after(self, *deps, status: str = 'success') -> None:
        assert status in ['any', 'failure', 'success']

        for dep in deps:
            self.add_parent(dep, status)

    @property
    def waitfor(self) -> str:
        return self._waitfor

    @waitfor.setter
    def waitfor(self, mode: str = 'all') -> None:
        assert mode in ['all', 'any']

        self._waitfor = mode

    def ensure(self, condition: Callable) -> None:
        self.postconditions.append(condition)

    @cached_property
    def done(self) -> bool:
        if len(self.postconditions) > 0:
            is_done = True
            for postcondition in self.postconditions:
                sig = inspect.signature(postcondition)
                if len(sig.parameters) >= 1:
                    is_done &= all(map(postcondition, self.array))
                else:
                    is_done &= postcondition()
        else:
            is_done = False

        return is_done

    def prune(self) -> None:
        if self.pruned:
            return
        self.pruned = True

        disabled = {
            dep for dep, status in self.dependencies.items()
            if dep.disabled
        }

        # Attach dependencies of disabled dependencies to current node.
        for dep in disabled:
            self.rm_parent(dep)
            for parent in dep.dependencies:
                self.add_parent(parent)

        done = {
            dep for dep, status in self.dependencies.items()
            if dep.done
        }

        if self.waitfor == 'any' and done:
            for dep in self.dependencies:
                self.rm_parent(dep)
        elif self.waitfor == 'all':
            for dep in done:
                self.rm_parent(dep)

        for dep in self.dependencies:
            dep.prune()

        if self.array is not None and len(self.postconditions) > 0:
            pending = {
                i for i in self.array
                if not self._verify_postconditions(i)
            }
            if len(pending) < len(self.array):
                self.array = pending


def terminal_nodes(*roots, prune: bool = False) -> Set[Node]:
    def search(job: Job) -> Set[Node]:
        if len(job.children) == 0:
            leafs = {job}
        else:
            leafs = set()
            for child in job.children:
                leafs.update(search(child))

        return leafs

    leafs = set()

    for root in roots:
        leafs.update(search(root))

    if prune:
        for leaf in leafs:
            leaf.prune()

    return leafs
