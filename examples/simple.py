import time

from awflow import job, after, waitfor, ensure, schedule


@job
def a():
    print('a')
    time.sleep(3)
    print('a')
    raise Exception()

def check_something():
    return True

@ensure(check_something)
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

d.prune()  # Prune jobs whose postconditions have been satisfied.

schedule(d, backend='local')  # prints b b c42 d d
