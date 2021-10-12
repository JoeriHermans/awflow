r"""
Decorator implementation for the standalone backend.
"""

from __future__ import annotations

from awflow.node import Node

from typing import Callable



def cpus(node: Node, n: int) -> None:
    node['--cpus-per-task='] = str(n)


def memory(node: Node, memory: str) -> None:
    node['--mem='] = memory.upper()


def gpus(node: Node, n: int) -> None:
    node['--gres=gpu:'] = str(n)


def timelimit(node: Node, timelimit: str) -> None:
    node['--time='] = str(time)
