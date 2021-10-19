r"""
In this example we'll explore the potential parallelism.

Note: The time differences mentioned in this example will
only be noticable in a Slurm environment, as the standalone
executor does not currently exploit potential parallelism.
"""

import awflow as aw
import numpy as np
import time



num_tasks = 10

################################################################################
# Approach 1
################################################################################

def start_with_tasks():
    start_time = time.time()
    np.save("starttime-with-tasks.npy", start_time)


@aw.tasks(num_tasks)
@aw.dependency(start_with_tasks)
def generate_with_tasks(task_index):
    print("Generating with tasks {} / {}.".format((task_index + 1), num_tasks))


@aw.tasks(num_tasks)
@aw.dependency(start_with_tasks)
def process_after_generation_with_task(task_index):
    print("Processing after generation with task {} / {}.".format((task_index + 1), num_tasks))


@aw.dependency(generate_with_tasks)
@aw.dependency(process_after_generation_with_task)
@aw.postcondition(aw.exists("time-with-tasks.npy"))  # Don't execute if file exists
def after_with_tasks():
    start_time = np.load("starttime-with-tasks.npy")
    duration = time.time() - start_time
    print("Duration", duration, "seconds.")
    np.save("time-with-tasks.npy", duration)


aw.execute()


################################################################################
# Approach 2
################################################################################

# TODO Implement


if __name__ == '__main__':
    aw.execute()
