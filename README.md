Reusable acyclic workflows in Python. Execute code on HPC systems as if you executed them on your machine!

## Motivation

Would you like fully reproducable research or workflows that seamlessly run on HPC clusters?
Tired of writing and managing large Slurm submission scripts? Do you have comment out large parts of your pipeline whenever its results have been generated?
Don't waste your precious time! `awflow` allows you to directly describe complex pipelines in Python, that run on your personal computer and large HPC clusters.


```python
import awflow as aw
import glob
import numpy as np

n = 100000
tasks = 10

@aw.cpus(4)  # Request 4 CPU cores
@aw.memory("4GB")  # Request 4 GB of RAM
@aw.postcondition(aw.num_files('pi-*.npy', 10))
@aw.tasks(tasks)  # Requests '10' parallel tasks
def estimate(task_index):
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
```
Executing this Python program (`python examples/pi.py`) on a Slurm HPC cluster will launch the following jobs.
```
           1803299       all    merge username PD       0:00      1 (Dependency)
           1803300       all show_res username PD       0:00      1 (Dependency)
     1803298_[6-9]       all estimate username PD       0:00      1 (Resources)
         1803298_3       all estimate username  R       0:01      1 compute-xx
         1803298_4       all estimate username  R       0:01      1 compute-xx
         1803298_5       all estimate username  R       0:01      1 compute-xx
```

Check the [examples](examples/) directory and [guide](examples/guide) to explore the functionality.

## Installation

The `awflow` package is available on [PyPi](https://pypi.org/project/awflow/), which means it is installable via `pip`.
```console
you@local:~ $ pip install awflow
```
If you would like the latest features, you can install it using this Git repository.
```console
you@local:~ $ pip install git+https://github.com/JoeriHermans/awflow
```
If you would like to run the examples as well, be sure to install the *optional* example dependencies.
```console
you@local:~ $ pip install 'awflow[examples]'
```
## Usage
The core concept in `awflow` is the notion of a task.
Essentially, this is a method that will be executed in your workflow.
Tasks are represented as a node in a directed graph. In doing so,
we can easily specify (task) dependencies. In addition, we can attribute
properties to tasks using decorators defined by `awflow`. This
allows you to specify things like CPU cores, GPU's and even postconditions.
Follow the [guide](examples/guide) for additional examples and descriptions.

### Decorators

TODO

## The `awflow` utility

This package comes with a utility program to manage submitted, failed, and pending workflows. Its functionality can be inspected by executing `awflow -h`. In addition, to streamline the management of workflows, we recommend to give every workflow as specific name to easily identify a workflow. This name does not have to be unique for every distinct workflow execution.
```python
aw.execute(name=r'Some name')
```
Executing `awflow list` after submitting the pipeline with `python pipeline.py [args]` will yield.
```console
you@local:~ $ awflow list
  Postconditions      Status      Backend     Name          Location
 ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  50%                 Running     Slurm       Some name     /home/jhermans/awflow/examples/.workflows/tmpntmc712a
```

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

### Roadmap

- [ ] Documentation
- [ ] README

## License

As described in the [`LICENSE`](LICENSE.txt) file.
