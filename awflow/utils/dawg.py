r"""
Utilities for Directed Acyclic Workflow Graphs.
"""

from __future__ import annotations

import awflow

from awflow.node import Node
from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG

from typing import Callable



def add_and_get_node(f: Callable) -> Node:
    r"""
    Adds a workflow node to the workflow compute graph.
    """
    # Is the function already in the workflow?
    node = awflow.workflow.find_node(f)
    if node is None:
        node = Node(f)
        awflow.workflow.add(node)

    return node
