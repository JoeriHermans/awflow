import argparse
import awflow
import os
import rich
import rich.pretty
import sys



def main() -> None:
    rich.pretty.install()
    module, arguments = _parse_arguments()
    module_handlers = {
        'list': _module_list}
    if module not in module_handlers.keys():
        raise ValueError('Module `{mod}` is unknow, execute `awflow -h`.'.format(
            mod=module))
    module_handlers[module](arguments)


def _module_list(arguments):
    print("Listing modules!")


def _parse_arguments():
    parser = argparse.ArgumentParser(
        prog='awflow',
        description='Manage workflows with ease.',
        epilog='For help or bugreports please refer to ' + awflow.__github__)
    # Specify the custom arguments
    # TODO

    # Verify
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    # Parse the program arguments
    arguments, unknown_arguments = parser.parse_known_args()
    module = unknown_arguments[0]

    return module, arguments
