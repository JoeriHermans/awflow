r"""Pythonic reusable Workflows. Execute code on HPC systems as if you
executed them on your laptop!

Predefined workflows and utilities to build dependency graphs on your local
workstation and HPC clusters.

Workflows are acyclic computational graphs which essentially define a dependency graph
of procedures. These graph serve as an abstraction for `executors`, which execute the
workflow locally or generate the required code to run the computational graph on an
HPC cluster without having to write the necessarry supporting code. Everything can
directly be done in Python.
"""

__name__ = "baum"
__version__ = "0.0.1"
__author__ = [
    "Joeri Hermans"]

__email__ = [
    "joeri@peinser.com"]


context = None


################################################################################
# Baum workflows
################################################################################
import baum.workflow


################################################################################
# Baum workflow decorators
################################################################################
from baum.decorator import *


################################################################################
# Baum utilities
################################################################################
import baum.util
