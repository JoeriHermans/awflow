import argparse
import numpy as np
import os

from awflow import after, ensure, job, schedule



n = 10000
tasks = 10


@ensure(lambda i: os.path.exists(f'pi-{i}.npy'))
@job(cpus='4', memory='4GB', array=tasks)
def estimate(i):
    print(f'Executing task {i + 1} / {tasks}.')
    x = np.random.random(n)
    y = np.random.random(n)
    pi_estimate = (x**2 + y**2 <= 1)
    np.save(f'pi-{i}.npy', pi_estimate)


@after(estimate)
@job(cpus='4')
def merge():
    files = glob.glob('pi-*.npy')
    stack = np.vstack([np.load(f) for f in files])
    pi_estimate = stack.sum() / (n * tasks) * 4
    np.save('pi.npy', pi_estimate)
    print(pi_estimate)

merge.prune()

schedule(merge, backend='local')
