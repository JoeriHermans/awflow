import time

from awflow import job, after, waitfor, ensure, schedule



@job
def a():
    print('a')
    time.sleep(3)
    print('a')
    raise Exception()

def check():
    return True

@ensure(check)
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


terminal_nodes = []


for attempt in range(5):

    @after(d)
    @job
    def e(index=attempt):
        print(index)
    terminal_nodes.append(e)

for node in terminal_nodes:
    node.prune()

schedule(*terminal_nodes, backend='local')  # prints a b b c42 a d d
