r"""
Decorator implementation for the standalone backend.
"""

from __future__ import annotations

from awflow.node import Node

from typing import Callable



def cpus(node: Node, n: int) -> None:
    raise NotImplementedError


def memory(node: Node, memory: str) -> None:
    raise NotImplementedError


def gpus(node: Node, n: int) -> None:
    raise NotImplementedError


def timelimit(node: Node, timelimit: str) -> None:
    raise NotImplementedError
