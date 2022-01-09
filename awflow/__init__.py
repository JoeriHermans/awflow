r"""
The awflow package contains modules and data structures to represent
and execute directed acyclic workflows. The workflows can be run on
your laptop, or when requested, code will be specifically generated
to run the workflows on HPC clusters without the need to specify
those annoying submission scripts.
"""

import os



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
