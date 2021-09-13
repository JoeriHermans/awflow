r"""Hypothesis is a python module for statistical inference and the
mechanisation of science.

The package contains (approximate) inference algorithms to solve inverse
statistical problems. Utilities are provided for data loading, efficient
simulation, visualization, fire-and-forget inference, and validation.

.. include:: ./documentation.md
"""

__name__ = "hypothesis"
__version__ = "0.4.0"
__author__ = [
    "Joeri Hermans"]

__email__ = [
    "joeri@peinser.com"]


###############################################################################
# Hypothesis' defaults
###############################################################################

import hypothesis.default


###############################################################################
# Hypothesis' utilities
###############################################################################

import hypothesis.util

###############################################################################
# Hypothesis' exception
###############################################################################

import hypothesis.exception

###############################################################################
# Hypothesis' engine
###############################################################################

import hypothesis.engine

###############################################################################
# Hypothesis' neural network utilities
###############################################################################

import hypothesis.nn

###############################################################################
# Hypothesis' default benchmarks
###############################################################################

import hypothesis.benchmark

###############################################################################
# Hypothesis' engine
###############################################################################

import hypothesis.engine

###############################################################################
# Hypothesis' inference
###############################################################################

import hypothesis.inference

###############################################################################
# Hypothesis' workflow
###############################################################################

import hypothesis.workflow

###############################################################################
# Hypothesis' plotting
################################################################################

import hypothesis.plot

###############################################################################
# Logging
###############################################################################

import logging
import coloredlogs

coloredlogs.install()

###############################################################################
# Global variables
###############################################################################

import multiprocessing
import torch

cpu_count = multiprocessing.cpu_count()
"""Number of available logical processor cores.

The variable will be initialized when ``hypothesis`` is loaded for the first time.
"""


workers = cpu_count
"""Default number of parallel workers in ``hypothesis``."""


def set_workers(n):
    r"""Sets the number of default parallel hypothesis workers."""
    assert n >= 1
    hypothesis.workers = n


accelerator = torch.device("cuda" if torch.cuda.is_available() else "cpu")
"""PyTorch device describing the accelerator backend.

The variable will be initialized when ``hypothesis`` is loaded for the first
time. It will check for the availibility of a CUDA device. If a CUDA enabled
device is present, ``hypothesis`` will select the CUDA device defined in the
``CUDA_VISIBLE_DEVICES`` environment variable. If no such device is specified,
the variable will default to GPU 0.
"""


def disable_gpu():
    r"""Disables GPU acceleration. Hypothesis' accelerator will have been
    set to 'cpu'."""
    hypothesis.accelerator = "cpu"
    hypothesis.a = hypothesis.accelerator


def enable_gpu():
    r"""Tries to enable GPU acceleration. If a GPU is present, a CUDA
    device will be set, else it will default to 'cpu'."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    hypothesis.accelerator = device
    hypothesis.a = device

    return hypothesis.accelerator


def gpu_available():
    r"""Checks if GPU acceleration is available."""
    return hypothesis.accelerator != "cpu"
