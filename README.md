Pythonic reusable acyclic workflows. Execute code on HPC systems as if you executed them on your personal computer!

### Motivation

Tired of writing and managing Slurm submission scripts? Do you have comment out large parts of your pipeline whenever its results have been generated?
No more! `awflow` allows you to directly prototype in Python, on your laptop. The module will take of Slurm for you!


```python
import awflow as aw
import glob
import numpy as np

n = 100000
tasks = 10

@aw.cpus(4)  # Request 4 CPU cores
@aw.memory("4GB")  # Request 4 GB of RAM
@aw.tasks(tasks)  # Requests '100' parallel tasks
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

Executing this Python program on a Slurm-enabled HPC cluster will produce the following jobs.
```
           1803299       all    merge username PD       0:00      1 (Dependency)
           1803300       all show_res username PD       0:00      1 (Dependency)
     1803298_[6-9]       all estimate username PD       0:00      1 (Resources)
         1803298_3       all estimate username  R       0:01      1 compute-xx
         1803298_4       all estimate username  R       0:01      1 compute-xx
         1803298_5       all estimate username  R       0:01      1 compute-xx
```

### Roadmap

- [ ] Developer requirements
- [ ] Documentation
- [ ] Enforce acyclicity of compute graph
- [ ] Logging directory
- [ ] Postcondition utilities
- [ ] README
- [ ] Utility scripts to manage workflows running on Slurm.
