r"""Workflow subroutine processing."""

import awflow
import cloudpickle as pickle
import logging
import sys



def main():
    with open(sys.argv[1], 'rb') as f:
        subroutine = pickle.load(f)
    if len(sys.argv) > 2:
        task_index = int(sys.argv[2])
        subroutine(task_index)
    else:
        subroutine()


if __name__ == '__main__':
    main()
