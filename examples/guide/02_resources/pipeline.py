r"""
The purpose of this example is to demonstrate
the resource allocation of a workflow.

There is an important distinction to be made
between the 'standalone' and 'slurm' backend.
Within the 'standalone' backend, i.e., when
executing the graph on your laptop, these resource
properties will not be enforced. Hence, you'll be
able to use more. However, executing this example
on Slurm will give you the expected output.
"""

import awflow as aw
import os


@aw.cpus(1)
@aw.memory("1gb")  # Lower-case or upper-case, doesn't matter.
def nproc1():
    os.system('nproc')  # Returns 1


@aw.cpus(4)
@aw.memory("512MB")
def nproc4():
    os.system('nproc')  # Returns 4


@aw.cpus(4)
@aw.dependency(nproc4)
@aw.gpus(1)
@aw.memory("1GB")
@aw.timelimit("2-12:00:00")  # 2 days, and 12 hours.
def method_with_timelimit():
    print("Done!")


if __name__ == '__main__':
    aw.execute()
