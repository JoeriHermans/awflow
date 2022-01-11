r"""Acyclic Workflows

The awflow package contains modules and data structures to represent
and execute directed acyclic workflows. The workflows can be run on
your laptop, or when requested, code will be specifically generated
to run the workflows on HPC clusters without the need to specify
those annoying submission scripts.
"""


__version__ = '0.1.1'


## Verify Python requirements ##################################################

import sys

if sys.version_info < (3,):
    raise Exception('Python 2 had reached end-of-life and is not supported.')


## Decorators and other workflow utilities #####################################

from functools import partial
from typing import Callable, Union

from .schedulers import schedule
from .workflow import Job, leafs, roots


def after(*deps, status: str = 'success') -> Callable:
    def decorator(self: Job) -> Job:
        self.after(*deps, status=status)
        return self

    return decorator


def ensure(condition: Callable, when: str = 'after') -> Callable:
    def decorator(self: Job) -> Job:
        self.ensure(condition, when)
        return self

    return decorator


def job(f: Callable = None, /, **kwargs) -> Union[Callable, Job]:
    if f is None:
        return partial(job, **kwargs)
    else:
        return Job(f, **kwargs)


def waitfor(mode: str) -> Callable:
    def decorator(self: Job) -> Job:
        self.waitfor = mode
        return self

    return decorator
