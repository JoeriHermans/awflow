def is_iterable(item):
    r"""Checks whether the specified item is iterable.

    :param item: Any possible Python instance.
    :rtype: bool
    """
    return hasattr(item, "__getitem__")
