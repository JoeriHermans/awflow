import awflow
import time

from awflow import job, after, waitfor, disable, ensure, schedule, terminal_nodes


@job
def a():
    print('a')
    time.sleep(3)
    print('a')
    raise Exception()

def check_something():
    return True

@ensure(check_something)
@disable
@job
def b():
    time.sleep(1)
    print('b')
    time.sleep(1)
    print('b')

finished = [True] * 100
finished[42] = False

@after(a, status='any')
@after(b)
@ensure(lambda i: finished[i])
@job(array=100)
def c(i: int):
    print(f'c{i}')
    finished[i] = True

@after(b, c)
@job
def d():
    print('d')
    time.sleep(1)
    print('d')

@after(c)
@job
def e():
    print('e')

leafs = terminal_nodes(a, prune=True)  # Search for terminal nodes of `a` and prune automatically
print(leafs)  # prints {d, e}

schedule(*leafs, backend='local')  # prints a a c42 d e d (e is executed concurrently by asyncio)
