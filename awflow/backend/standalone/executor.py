r"""
Definition of the standalone executor.
"""

import os
import tempfile

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
        program = workflow.program()
        for node in program:
            return_code = execute_generated_code(dir=directory, node=node)
            if return_code != 0:  # Stop program execution on non-zero return code.
                break
    else:
        program = workflow.program()
        for node in program:
            execute_node(node)


def execute_generated_code(dir: str, node: Node) -> int:
    name = executable_name(node)
    command = 'eval "$(conda shell.bash hook)" && conda activate baum && python -u -m awflow.bin.processor ' + dir + '/' + name
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
