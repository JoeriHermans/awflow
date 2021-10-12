r"""
Generic utilities for compute backends.
"""

import shutil

from . import slurm
from . import standalone



def autodetect():
    if slurm_detected():
        return slurm

    return standalone


def slurm_detected() -> bool:
    output = shutil.which('sbatch')
    return output != None and len(output) > 0
