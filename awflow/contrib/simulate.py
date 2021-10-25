r"""
Utilities to aid in the generation of a large set of simulations.
"""

import awflow as aw
import numpy as np
import os

from typing import List


def generate(simulator, n, out='./data', blocks=100, cpus=1, memory='4GB', dependency=None) -> List:
    if blocks <= 1:
        raise ValueError('Number of simulation blocks have to be larger than 1.')

    assert n % blocks == 0
    blocksize = n // blocks
    dependencies = []
    out_blocks = out + '/blocks'
    os.makedirs(out_blocks, exist_ok=True)

    @aw.cpus(cpus)
    @aw.dependency(dependency)
    @aw.memory(memory)
    @aw.tasks(blocks)
    def simulate(task_index):
         simulate(blocksize, out_blocks + '/' + str(task_index).zfill(5))
    dependencies.append(simulate)

    return dependencies
