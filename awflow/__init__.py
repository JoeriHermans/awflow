r"""
The awflow package contains modules and data structures to represent
and execute directed acyclic workflows. The workflows can be run on
your laptop, or when requested, code will be specifically generated
to run the workflows on HPC clusters without the need to specify
those annoying submission scripts.
"""

import os
import sys



################################################################################
# Verify Python version
################################################################################
if sys.version_info < (3,):
    raise Exception('Python 2 had reached end-of-life and is not supported.')


################################################################################
# Global specifications
################################################################################
from .spec import __version__
from .spec import __github__


################################################################################
# Decorators
################################################################################
from functools import partial
from typing import Callable, Union

from .schedulers import schedule
from .workflow import Job



def job(f: Callable = None, /, **kwargs) -> Union[Callable, Job]:
    if f is None:
        return partial(job, **kwargs)
    else:
        return Job(f, **kwargs)


def after(*deps, status: str = 'success') -> Callable:
    def decorator(self: Job) -> Job:
        self.after(*deps, status=status)
        return self

    return decorator


def waitfor(mode: str) -> Callable:
    def decorator(self: Job) -> Job:
        self.waitfor = mode
        return self

    return decorator


def ensure(condition: Callable) -> Callable:
    def decorator(self: Job) -> Job:
        self.ensure(condition)
        return self

    return decorator


def disable(job: Job = None) -> Callable:
    job.disabled = True

    return job


################################################################################
# Backend utilities
################################################################################
from .schedulers import available_backends  # Yields the available backends


################################################################################
# Workflow utilities
################################################################################
from .workflow import terminal_nodes  # Yields the terminal nodes of a set of roots
