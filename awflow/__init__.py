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
# Version specification
################################################################################
from .version import __version__


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
    workflow.prune()
    if len(workflow.nodes) > 0:
        backend.execute(workflow=workflow, **kwargs)
