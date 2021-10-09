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
import awflow.utils

from awflow.decorators import *
from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG


################################################################################
# Default compute graph definition
################################################################################
workflow = DAWG()


################################################################################
# Autodetect compute backend and allocate its executor
################################################################################
executor = awflow.utils.backend.autodetect()
