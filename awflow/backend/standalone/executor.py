r"""
Definition of the standalone executor.
"""

import os
import tempfile
import awflow.hooks as hooks

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node
from awflow.utils.executor import generate_executables
from awflow.utils.executor import executable_name



def execute(workflow: DAWG, dir: str = '.workflows', **kwargs) -> None:
    # Check if code needs to be generated.
    generate_code = kwargs.get('generate_code', False)
    if generate_code:
        # Preparing the execution files.
        os.makedirs(dir, exist_ok=True)  # Create the base directory
        directory = tempfile.mkdtemp(dir=dir)
        # Generate the executables for the graph.
        generate_executables(workflow=workflow, dir=directory)
        # Execute the workflow in BFS (program) order.
        apply_defaults(workflow, **kwargs)
        program = workflow.program()
        for node in program:
            return_code = execute_generated_code(dir=directory, node=node)
            if return_code != 0:  # Stop program execution on non-zero return code.
                break
    else:
        program = workflow.program()
        for node in program:
            execute_node(node)


def apply_defaults(workflow: DAWG, **kwargs) -> None:
    apply_default_conda_environment(workflow, **kwargs)


def apply_default_conda_environment(workflow: DAWG, **kwargs) -> None:
    conda_environment = kwargs.get('conda', '')
    if len(conda_environment) == 0 and 'CONDA_DEFAULT_ENV' in os.environ:
        conda_environment = os.environ['CONDA_DEFAULT_ENV']
    if len(conda_environment) > 0:
        for node in workflow.nodes:
            hooks.conda.set_environment(node, conda_environment)


def execute_generated_code(dir: str, node: Node) -> int:
    # Prepare the commands
    commands = []
    commands.extend(hooks.conda.generate_activate(node))
    commands.append('python -u -m awflow.bin.processor ' + dir + '/' + executable_name(node))
    # Generate the command string
    command = ' && '.join(commands)
    if node.tasks > 1:
        for task_index in range(node.tasks):
            task_command = command + ' ' + str(task_index)
            return_code = os.system(task_command)
    else:
        return_code = os.system(command)

    return return_code


def execute_node(node: Node) -> None:
    if node.tasks > 1:
        for task_index in range(node.tasks):
            node.f(task_index)
    else:
        node.f()
