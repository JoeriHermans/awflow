r"""
The awflow package contains modules and data structures to represent
and execute directed acyclic workflows. The workflows can be run on
your laptop, or when requested, code will be specifically generated
to run the workflows on HPC clusters without the need to specify
those annoying submission scripts.
"""

import os
import sys
import time



################################################################################
# Verify Python version
################################################################################
if sys.version_info < (3,):
    raise Exception('Python 2 had reached end-of-life and is not supported.')


################################################################################
# Increase recursion depth (to handle large workflow graph pruning)
################################################################################
sys.setrecursionlimit(10000)


################################################################################
# Global specifications
################################################################################
from .spec import __version__
from .spec import __github__


################################################################################
# Autoload imports
################################################################################
from . import utils
from . import backends


################################################################################
# Default computational graph definition
################################################################################
from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG

workflow = DAWG()  # Too bad there is a PyPi package called `dawg`.


################################################################################
# Load the plugins module
################################################################################
from . import plugins


################################################################################
# Load the function decorators
################################################################################
from .decorators import *


################################################################################
# Set the compute backend
################################################################################
backend = backends.autodetect()

def execute(**kwargs) -> None:
    workflow.metadata['args'] = sys.argv[1:]
    workflow.metadata['datetime'] = time.time()
    workflow.metadata['name'] = kwargs.get('name', '')
    workflow.metadata['pipeline'] = sys.argv[0]
    workflow.metadata['version'] = __version__
    workflow.prune()
    if len(workflow.nodes) > 0:
        backend.execute(workflow=workflow, **kwargs)
    workflow.clear()

def clear() -> None:
    workflow.clear()
