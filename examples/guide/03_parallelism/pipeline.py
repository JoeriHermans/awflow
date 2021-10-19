r"""
In this example we'll explore the potential parallelism.

Note: The time differences mentioned in this example will
only be noticable in a Slurm environment, as the standalone
executor does not currently exploit potential parallelism.
"""

import argparse
import awflow as aw
import numpy as np
import os
import time


parser = argparse.ArgumentParser('awflow guide: Parallelism')
parser.add_argument('--partition', type=str, default=None, help='Slurm partition to execute workflow on (default: default Slurm partition).')
parser.add_argument('--reset', action='store_true', default=False, help='Reset the pipeline by clearing all its postconditions (default: false).')
parser.add_argument('--tasks', type=int, default=25, help='Number of parallel tasks for every stage (default: 25).')
arguments, _ = parser.parse_known_args()


# Check if files have to be reset
if arguments.reset:
    os.system('rm *.npy')


################################################################################
# Approach 1
################################################################################

def start_with_tasks():
    start_time = time.time()
    np.save('starttime-with-tasks.npy', start_time)


@aw.tasks(arguments.tasks)
@aw.dependency(start_with_tasks)
def generate_with_tasks(task_index):
    print('Generating with tasks {} / {}.'.format((task_index + 1), arguments.tasks))


@aw.tasks(arguments.tasks)
@aw.dependency(generate_with_tasks)
def process_after_generation_with_task(task_index):
    print('Processing after generation with task {} / {}.'.format((task_index + 1), arguments.tasks))


@aw.dependency(generate_with_tasks)
@aw.dependency(process_after_generation_with_task)
@aw.postcondition(aw.exists('time-with-tasks.npy'))  # Don't execute if file exists
def after_with_tasks():
    start_time = np.load('starttime-with-tasks.npy')
    duration = time.time() - start_time
    print('Duration', duration, 'seconds.')
    np.save('time-with-tasks.npy', duration)


aw.execute(partition=arguments.partition)


################################################################################
# Approach 2
################################################################################

def start():
    start_time = time.time()
    np.save('starttime.npy', start_time)


dependencies = []
for task_index in range(arguments.tasks):

    @aw.dependency(start)
    def generate(task_index=task_index):
        print('Generating {} / {}.'.format((task_index + 1), arguments.tasks))

    @aw.dependency(generate)
    def process(task_index=task_index):
        print('Processing after generation {} / {}.'.format((task_index + 1), arguments.tasks))

    dependencies.append(process)


@aw.dependency(dependencies)
@aw.postcondition(aw.exists('time.npy'))
def after():
    start_time = np.load('starttime.npy')
    duration = time.time() - start_time
    print('Duration', duration, 'seconds.')
    np.save('time.npy', duration)


aw.execute(partition=arguments.partition)
