import argparse
import awflow
import glob
import sys
import numpy as np
import os

from awflow import after, ensure, job, schedule



# Prepare argument parser
parser = argparse.ArgumentParser('awflow π demo.')
parser.add_argument('--backends', action='store_true', help='Shows the available backends and exits.')
parser.add_argument('--backend', type=str, default='local', help='Compute backend (default: local).')
parser.add_argument('--partition', type=str, default=None, help='Partition to deploy the jobs on and can only be specified through the Slurm backend (default: none).')
arguments, _ = parser.parse_known_args()

if arguments.backends:
    print(awflow.available_backends())

# Script parameters
n = 10000
tasks = 25


@ensure(lambda i: os.path.exists(f'pi-{i}.npy'))
@job(cpus='4', memory='4GB', array=tasks)
def estimate(i):
    print(f'Executing task {i + 1} / {tasks}.')
    x = np.random.random(n)
    y = np.random.random(n)
    pi_estimate = (x**2 + y**2 <= 1)
    np.save(f'pi-{i}.npy', pi_estimate)

@after(estimate)
@ensure(lambda: os.path.exists('pi.npy'))
@job(cpus='4', name='merge_and_show')  # Ability to overwrite job name
def merge():
    files = glob.glob('pi-*.npy')
    stack = np.vstack([np.load(f) for f in files])
    pi_estimate = stack.sum() / (n * tasks) * 4
    print('π ≅', pi_estimate)
    np.save('pi.npy', pi_estimate)

merge.prune()

schedule(merge, backend=arguments.backend, partition=arguments.partition)
if arguments.backend == 'slurm':
    print("Jobs have been submitted!")
