r"""
Definition of Directed Acyclic Workflow Graph (DAWG).
"""

from __future__ import annotations

from awflow.node import Node

from typing import Any
from typing import Callable
from typing import Union


class DirectedAcyclicWorkflowGraph:

    def __init__(self):
        super(DirectedAcyclicWorkflowGraph, self).__init__()
        self._nodes = {}

    def add(self, node: Node) -> None:
        self._nodes[node.identifier] = node

    def find_node(self, f: Callable) -> Union[Node, None]:
        try:
            node = self._nodes[id(f)]
        except:
            node = None

        return node

    @property
    def nodes(self) -> list[Node]:
        return self._nodes.values()

    @property
    def roots(self) -> list[Node]:
        roots = []
        for node in self.nodes:
            if len(node.parents) == 0:
                roots.append(node)

        return roots
