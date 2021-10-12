r"""
Decorator implementation for the standalone backend.
"""

from __future__ import annotations

from awflow.node import Node

from typing import Callable



def cpus(node: Node, n: int) -> None:
    pass  # Nothing to do here.


def memory(node: Node, memory: str) -> None:
    pass  # Nothing to do here.


def gpus(node: Node, n: int) -> None:
    pass  # Nothing to do here.


def timelimit(node: Node, timelimit: str) -> None:
    pass  # Nothing to do here.
