Reproducible research and reusable acyclic workflows in Python. Execute code on HPC systems as if you executed them on your machine!

## Motivation

Would you like fully reproducible research or reusable workflows that seamlessly run on HPC clusters?
Tired of writing and managing large Slurm submission scripts? Do you have comment out large parts of your pipeline whenever its results have been generated? Hate YAML?
Don't waste your precious time! `awflow` allows you to directly describe complex pipelines in Python, that run on your personal computer and large HPC clusters.


```python
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

merge.prune()  # Prune dependencies whose postconditions have already been satisfied.

schedule(merge, backend='local')  # Uses the local compute backend
```
Executing this Python program (`python examples/pi.py --slurm`) on a Slurm HPC cluster will launch the following jobs.
```
           1803299       all    merge username PD       0:00      1 (Dependency)
           1803300       all show_res username PD       0:00      1 (Dependency)
     1803298_[6-9]       all estimate username PD       0:00      1 (Resources)
         1803298_3       all estimate username  R       0:01      1 compute-xx
         1803298_4       all estimate username  R       0:01      1 compute-xx
         1803298_5       all estimate username  R       0:01      1 compute-xx
```

Check the [examples](examples/) directory to explore the functionality.

## Usage

TODO

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

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

As described in the [`LICENSE`](LICENSE.txt) file.
