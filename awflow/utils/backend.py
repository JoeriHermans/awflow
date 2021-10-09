r"""
Generic utilities for compute backends.
"""

import awflow
import awflow.backend
import shutil



def autodetect():
    # Detect Slurm
    if slurm_detected():
        return awflow.backend.slurm

    return awflow.backend.standalone


def slurm_detected() -> bool:
    output = shutil.which('sbatch')
    return output != None and len(output) > 0
