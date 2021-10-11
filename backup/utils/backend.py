r"""
Generic utilities for compute backends.
"""

import shutil



def autodetect():
    if slurm_detected():
        return 'slurm'

    return 'standalone'


def slurm_detected() -> bool:
    output = shutil.which('sbatch')
    return output != None and len(output) > 0


def available_backends() -> list[str]:
    backends = ['standalone']

    if slurm_detected():
        backends.append('slurm')

    return backends
