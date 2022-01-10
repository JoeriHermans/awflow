r"""Scheduler backends."""

import asyncio
import cloudpickle as pickle
import contextvars
import os

from abc import ABC, abstractmethod
from datetime import datetime
from functools import partial
from pathlib import Path
from subprocess import run
from typing import Any, Callable, Dict, List

from .workflow import Job



class CyclicDependencyGraphError(Exception):
    pass


class DependencyNeverSatisfiedException(Exception):
    pass


class JobNotFailedException(Exception):
    pass


class BaseScheduler(ABC):
    r"""Abstract workflow scheduler."""

    def __init__(self):
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


def schedule(*jobs, backend: str = None, **kwargs) -> List[Any]:
    scheduler = {
        'local': LocalScheduler,
    }.get(backend)(**kwargs)

    return asyncio.run(scheduler.gather(*jobs))
