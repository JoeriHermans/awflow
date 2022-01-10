r"""Scheduler backends."""

import asyncio
import cloudpickle as pickle
import contextvars
import os
import shutil

from abc import ABC, abstractmethod
from datetime import datetime
from functools import lru_cache
from functools import partial
from pathlib import Path
from subprocess import run
from typing import Any, Callable, Dict, List

from .workflow import Job



class DependencyNeverSatisfiedException(Exception):
    pass


class JobNotFailedException(Exception):
    pass


class BaseScheduler(ABC):
    r"""Abstract workflow scheduler."""

    def __init__(self, **kwargs):
        self.submissions = {}

    async def gather(self, *jobs) -> List[Any]:
        return await asyncio.gather(*map(self.submit, jobs))

    async def submit(self, job: Job) -> Any:
        if job not in self.submissions:
            self.submissions[job] = asyncio.create_task(self._submit(job))

        return await self.submissions[job]

    @abstractmethod
    async def _submit(self, job: Job) -> Any:
        pass


class LocalScheduler(BaseScheduler):
    r"""Local scheduler."""

    async def condition(self, job: Job, status: str) -> Any:
        result = await self.submit(job)

        if isinstance(result, Exception):
            if status == 'success':
                return result
            else:
                return None
        else:
            if status == 'failure':
                raise JobNotFailedException(f'{job}')
            else:
                return result

    async def _submit(self, job: Job) -> Any:
        # Wait for (all or any) dependencies to complete
        pending = {
            asyncio.create_task(self.condition(dep, status))
            for dep, status in job.dependencies.items()
        }

        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                result = task.result()

                if isinstance(result, Exception):
                    if job.waitfor == 'all':
                        raise DependencyNeverSatisfiedException(f'aborting job {job}') from result
                else:
                    if job.waitfor == 'any':
                        break
            else:
                continue
            break
        else:
            if job.dependencies and job.waitfor == 'any':
                raise DependencyNeverSatisfiedException(f'aborting job {job}')

        # Execute job
        try:
            if job.array is None:
                return await to_thread(job.fn)
            else:
                return await asyncio.gather(*(
                    to_thread(job.fn, i)
                    for i in job.array
                ))
        except Exception as error:
            return error


class SlurmScheduler(BaseScheduler):
    r"""Scheduler for the Slurm workload manager."""

    def __init__(
        self,
        *jobs,
        name: str = None,
        path: str = '.workflows',
        **kwargs,
    ):
        super().__init__(*jobs, **kwargs)
        if name is None:
            name = datetime.now().strftime('%y%m%d_%H%M%S')
        path = Path(path) / name
        path.mkdir(parents=True, exist_ok=True)

        self.name = name
        self.partition = kwargs.get('partition', None)
        self.path = path.resolve()
        self.table = {}

    def id(self, job: Job) -> str:
        identifier = str(id(job))
        self.table[identifier] = job

        return identifier

    async def _submit(self, job: Job) -> str:
        # Wait for the dependencies to be submitted.
        jobids = await asyncio.gather(*[
            self.submit(dep)
            for dep in job.dependencies
        ])

        # Prepare the submission file.
        lines = [
            f"#!{os.environ['SHELL']}",
            '#',
            f'#SBATCH --job-name={job.name}',
            '#SBATCH --export=ALL',
            '#SBATCH --parsable',
            '#SBATCH --requeue',
        ]

        # Set the job partition
        if self.partition:
            lines.append(f'#SBATCH --partition={self.partition}')

        # Prepare the potential array job and the logfile.
        if job.array is None:
            logfile = self.path / f'{job.name}_%j.log'
        else:
            array = job.array
            if type(array) is range:
                lines.append('#SBATCH --array=' + f'{array.start}-{array.stop-1}:{array.step}')
            else:
                lines.append('#SBATCH --array=' + ','.join(map(str, array)))
            logfile = self.path / f'{job.name}_%j_%a.log'
        lines.append(f'#SBATCH --output={logfile}')

        # Specify the resources.
        translate = {
            'cpus': 'cpus-per-task',
            'gpus': 'gpus-per-task',
            'memory': 'mem',
            'timelimit': 'time',
        }
        for key, value in job.settings.items():
            key = translate.get(key, key)
            if value is None:
                lines.append(f'#SBATCH --{key}')
            else:
                lines.append(f'#SBATCH --{key}={value}')

        # Specify job dependencies.
        separator = '?' if job.waitfor == 'any' else ','
        keywords = {
            'success': 'afterok',
            'failure': 'afternotok',
            'any': 'afterany',
        }
        deps = [
            f'{keywords[status]}:{jobid}'
            for jobid, (_, status) in zip(jobids, job.dependencies.items())
        ]
        if deps:
            lines.append('#SBATCH --dependency=' + separator.join(deps))

        # Dump the job and add the executor to the script.
        pklfile = self.path / f'{self.id(job)}.pkl'
        with open(pklfile, 'wb') as f:
            f.write(pickle.dumps(job.fn))
        command = f'python -m awflow.bin.processor {pklfile}'
        if job.array is not None:
            command += ' $SLURM_ARRAY_TASK_ID'
        lines.append(command)

        # Save the generated script
        bashfile = self.path / f'{self.id(job)}.sh'
        with open(bashfile, 'w') as f:
            f.write('\n'.join(lines))

        # Submit job
        output = run(['sbatch', str(bashfile)], capture_output=True, check=True, text=True).stdout
        for jobid in output.splitlines():
            return jobid


async def to_thread(func: Callable, /, *args, **kwargs) -> Any:
    r"""Asynchronously run function `func` in a separate thread.

    Any *args and **kwargs supplied for this function are directly passed
    to `func`. Also, the current `contextvars.Context` is propagated,
    allowing context variables from the main thread to be accessed in the
    separate thread.

    Return a coroutine that can be awaited to get the eventual result of `func`.

    References:
        https://github.com/python/cpython/blob/main/Lib/asyncio/threads.py
    """

    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = partial(ctx.run, func, *args, **kwargs)

    return await loop.run_in_executor(None, func_call)


def schedule(*jobs, backend: str, **kwargs) -> List[Any]:
    assert backend in available_backends()

    jobs = filter(lambda job: not job.done and not job.disabled, jobs)  # Filter terminal nodes whose postconditions have been satisfied.
    scheduler = {
        'local': LocalScheduler,
        'slurm': SlurmScheduler,
    }.get(backend)(**kwargs)

    return asyncio.run(scheduler.gather(*jobs))


def detect_slurm() -> bool:
    output = shutil.which('sbatch')
    return output != None and len(output) > 0


@lru_cache(maxsize=None)  # @cache from Python 3.9
def available_backends() -> List['str']:
    backends = ['local']
    if detect_slurm():
        backends.append('slurm')

    return backends
