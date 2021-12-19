import argparse
import awflow
import os
import rich
import sys

from awflow.bin.cli.utils import print_error



def main() -> None:
    module, unknown_args, args = _parse_arguments()
    module_handlers = {
        'cancel': _module_cancel,
        'list': _module_list}
    if module not in module_handlers.keys():
        raise ValueError('Module `{mod}` is unknow, execute `awflow -h`.'.format(
            mod=module))
    module_handlers[module](unknown_args, args)


def _module_cancel(unknown_args, args):
    if not awflow.backends.utils.slurm_detected():
        print_error('You can only cancel workflows running on a Slurm cluster.')
        sys.exit(1)
    ## TODO Implement


def _module_list(unknown_args, args):
    root = os.path.abspath(args.pipeline + '/.workflows')
    if os.path.exists(root):
        workflow_directories = [os.path.abspath(f) for f in os.listdir(root) if os.path.isdir(f)]
    else:
        print_error('[bold red]No workflows found![/bold red]')
        sys.exit(1)


def _parse_arguments():
    parser = argparse.ArgumentParser(
        prog='awflow',
        description='Manage reproducable workflows with ease.',
        epilog='For help or bugreports please refer to ' + awflow.__github__)
    # Specify the custom arguments
    parser.add_argument('--pipeline', type=str, default='.', help='Specify directory of the pipeline (default: current directory).')

    # Verify
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # Parse the program arguments
    arguments, unknown_arguments = parser.parse_known_args()
    module = unknown_arguments[0]
    del unknown_arguments[0]

    return module, unknown_arguments, arguments
