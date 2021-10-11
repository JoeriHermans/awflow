r"""
Utility functions specifically related to decorators.
"""

from typing import Callable



def parameterized(decorator: Callable) -> Callable:
    r"""A decorator of a :attr:`decorator` specification to indicate
    that the decorator it is defining is parameterized, i.e.,
    it can accept arguments.

    Args
        decorator: A callable function which specifies the definition
            of the decorator you would like to be able to parameterize.

    Returns
        A decorator that is parameterizable.
    """
    def layer(*args, **kwargs):
        def reply(function):
            return decorator(function, *args, **kwargs)
        return reply
    return layer
