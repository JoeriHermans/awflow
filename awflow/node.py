r"""
Nodes are abstract representation of subprograms that are executed.
In essence, they are the decorated functions that are executed as
singilar entities. Nodes can be annotated with various properties
to define their behaviour and necessary resources.
"""

from __future__ import annotations

from typing import Any
from typing import Callable



class Node:

    def __init__(self, function: Callable):
        super(Node, self).__init__()
        self.f = function
        self._attributes = {}
        self._children = set()
        self._parents = set()
        self._postconditions = []
        self._prunable = False
        self._tasks = 1

    @property
    def postconditions(self) -> list[Callable]:
        return self._postconditions

    def add_postcondition(self, f: Callable) -> None:
        self._postconditions.append(f)

    def magic(self) -> None:
        if self.prunable:
            return
        self._magic_postconditions()

    def _magic_postconditions(self) -> None:
        # Verify if the postconditions are satisfied.
        if len(self._postconditions) > 0:
            postconditions_satsified = True
            for postcondition in self._postconditions:
                if not postcondition():
                    postconditions_satsified = False
                    break
            if postconditions_satsified:
                def set_prunable(node):
                    node.prunable = True
                    for p in node.parents:
                        set_prunable(p)
                set_prunable(self)

    @property
    def attributes(self) -> dict:
        return self._attributes

    @property
    def identifier(self) -> int:
        return id(self.f)

    @property
    def tasks(self) -> int:
        return self._tasks

    @tasks.setter
    def tasks(self, value: int) -> None:
        if value <= 0:
            raise ValueError("A node requires at least a single task.")
        self._tasks = value

    @property
    def name(self) -> str:
        if "name" in self._attributes.keys():
            name = self._attributes["name"]
        else:
            name = self.f.__name__

        return name

    @name.setter
    def name(self, value: str) -> None:
        self._attributes["name"] = value

    @property
    def prunable(self) -> bool:
        return self._prunable

    @prunable.setter
    def prunable(self, prunable: bool) -> None:
        self._prunable = prunable

    @property
    def parents(self) -> set[Node]:
        return self._parents

    @parents.setter
    def parents(self, parents: list[Node]) -> None:
        self._parents = set(parents)

    def add_parent(self, node: Node) -> None:
        if node is not None:
            self._parents.add(node)
            node._children.add(self)

    def remove_parent(self, node: Node) -> None:
        self._parents.remove(node)
        node._children.remove(self)

    def add_child(self, node: Node) -> None:
        if node is not None:
            self._children.add(node)
            node._parents.add(self)

    def remove_child(self, node: Node) -> None:
        self._children.remove(node)
        node._parents.remove(self)

    @property
    def dependencies(self) -> set[Node]:
        return self.parents

    def add_dependency(self, node: Node) -> None:
        self.add_parent(node)

    @property
    def children(self) -> set[Node]:
        return self._children

    @children.setter
    def children(self, children: list[Node]) -> None:
        self._children = set(children)

    def __del__(self) -> None:
        parents = list(self.parents)  # Make copy of parents
        children = list(self.children)  # Make copy of children
        for parent in parents:
            parent.remove_child(self)
        for child in children:
            child.remove_parent(self)

    def __setitem__(self, key: Any, value: Any) -> None:
        self._attributes[key] = value

    def __getitem__(self, key: Any) -> Any:
        return self._attributes[key]
