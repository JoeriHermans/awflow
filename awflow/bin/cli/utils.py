import rich

from rich import print


def print_error(msg):
    print('[bold red]{msg}[/bold red]'.format(msg=msg))
