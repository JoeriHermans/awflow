r"""
Utility decorators.
"""

import glob
import os

from typing import Callable



def exists(path: str) -> Callable:
    def wrapper() -> bool:
        return os.path.exists(path)

    return wrapper


def not_exists(path: str) -> Callable:
    def wrapper() -> bool:
        return not os.path.exists(path)

    return wrapper


def num_files(query: str, n) -> Callable:
    def wrapper() -> bool:
        return len(glob.glob(query)) == n

    return wrapper


def at_least_num_files(query, n) -> Callable:
    def wrapper() -> bool:
        return len(glob.glob(query)) >= n

    return wrapper
