r"""
Definition of the standalone executor.
"""

import os
import tempfile

from awflow import plugins
from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node
from awflow.utils.executor import executable_name
from awflow.utils.executor import generate_executables
from awflow.utils.executor import generate_metadata
from awflow.utils.executor import generate_postconditions



def execute(workflow: DAWG, dir: str = '.workflows', **kwargs) -> None:
    # Preparing the execution files.
    os.makedirs(dir, exist_ok=True)  # Create the base directory
    directory = os.path.abspath(tempfile.mkdtemp(dir=dir))
    program = workflow.program()
    plugins.apply_defaults(workflow=workflow, **kwargs)
    # Generate the necessary files for the graph execution.
    generate_executables(workflow=workflow, dir=directory)
    generate_metadata(workflow=workflow, dir=directory)
    generate_postconditions(workflow=workflow, dir=directory)
    # Execute the workflow in BFS (program) order.
    program = workflow.program()
    for node in program:
        return_code = execute_node(node=node, dir=directory)
        if return_code != 0:
            exit(return_code)


def execute_node(node: Node, dir: str) -> int:
    # Prepare the commands
    commands = []
    commands.extend(plugins.generate_before(node=node))
    absolute_path = os.path.abspath(dir + '/' + executable_name(node))
    commands.append('python -u -m awflow.bin.processor ' + absolute_path)
    commands.extend(plugins.generate_after(node=node))
    # Generate the command string
    command = ' && '.join(commands)
    if node.tasks > 1:
        for task_index in range(node.tasks):
            task_command = command + ' ' + str(task_index)
            return_code = os.system(task_command)
            if return_code != 0:
                break
    else:
        return_code = os.system(command)

    return return_code
