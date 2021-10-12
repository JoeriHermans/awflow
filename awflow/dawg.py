r"""
Definition of Directed Acyclic Workflow Graph (DAWG).
"""

from __future__ import annotations

from awflow.node import Node

from typing import Any
from typing import Callable
from typing import Generator
from typing import List
from typing import Union

from queue import Queue


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

    def program(self) -> List[Node]:
        program = []
        for node in self.bfs():
            if node in program:
                continue
            program.append(node)

        return program

    def bfs(self) -> Generator[Node, None]:
        queue = Queue()
        if len(self.roots) > 0:
            for root in self.roots:
                queue.put(root)
            yield from self._bfs(queue)
        else:
            yield from []

    def prune(self) -> None:
        # Prepare the nodes
        for node in self.nodes:
            node.magic()
        previous_size = 0
        current_size = len(self.nodes)
        while previous_size != current_size:
            # Update properties before pruning
            previous_size = current_size
            # Prune the graph in program order.
            nodes = list(self.nodes)  # Make a copy, as we'll modify the graph.
            for node in nodes:
                if node.prunable:
                    children = list(node.children)
                    parents = list(node.parents)
                    # Connect all children to all parents.
                    for parent in parents:
                        for child in children:
                            parent.add_child(child)
                    # Remove node from graph
                    for parent in parents:
                        parent.remove_child(node)
                    for child in children:
                        child.remove_parent(node)
                    del self._nodes[id(node.f)]
                    break
            # Update properties after pruning
            current_size = len(self.nodes)

    def _bfs(self, queue: Queue) -> Generator[Node, None]:
        if not queue.empty():
            node = queue.get()
            yield node
            for child in node.children:
                queue.put(child)
            yield from self._bfs(queue)

    @property
    def nodes(self) -> list[Node]:
        return list(self._nodes.values())

    @property
    def roots(self) -> list[Node]:
        roots = []
        for node in self.nodes:
            if len(node.parents) == 0:
                roots.append(node)

        return roots
