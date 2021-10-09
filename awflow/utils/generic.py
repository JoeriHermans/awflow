r"""
Generic awflow utilities.
"""

from typing import Any



def is_iterable(item: Any) -> bool:
    r"""Checks whether the specified item is iterable.

    The method works by verifying whether :attr:`item`
    holds the `__getitem__` attribute.

    Args
        item: the item or object to verify.

    Returns
        Boolean indicating whether :attr:`item` is iterable.
    """
    return hasattr(item, "__getitem__")
