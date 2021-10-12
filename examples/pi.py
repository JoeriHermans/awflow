import awflow as aw
import glob
import numpy as np
import os

n = 100000
tasks = 10

@aw.cpus(4)  # Request 4 CPU cores
@aw.memory("4GB")  # Request 4 GB of RAM
@aw.tasks(tasks)  # Requests '100' parallel tasks
@aw.postcondition(aw.num_files('pi-*.npy', 10))  # Prevent execution if all files have been generated.
def estimate(task_index):
    if not os.path.exists('pi-{}.npy'.format(task_index)):
        print("Executing task {} / {}.".format(task_index + 1, tasks))
        x = np.random.random(n)
        y = np.random.random(n)
        pi_estimate = (x**2 + y**2 <= 1)
        np.save('pi-' + str(task_index) + '.npy', pi_estimate)

@aw.dependency(estimate)
def merge():
    files = glob.glob('pi-*.npy')
    stack = np.vstack([np.load(f) for f in files])
    np.save('pi.npy', stack.sum() / (n * tasks) * 4)

@aw.dependency(merge)
@aw.postcondition(aw.exists('pi.npy'))  # Prevent execution if postcondition is satisfied.
def show_result():
    print("Pi:", np.load('pi.npy'))

aw.execute()
