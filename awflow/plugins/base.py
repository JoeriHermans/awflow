import importlib

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node

from typing import List



plugins = [
    'awflow.plugins.chdir',
    'awflow.plugins.conda']



def apply_defaults(workflow: DAWG, **kwargs):
    for plugin in plugins:
        module = importlib.import_module(plugin)
        applier = getattr(module, 'apply_defaults')
        for node in workflow.nodes:
            applier(node, **kwargs)


def generate_before(node: Node) -> List[str]:
    commands = []

    for plugin in plugins:
        module = importlib.import_module(plugin)
        generator = getattr(module, 'generate_before')
        commands.extend(generator(node))

    return commands


def generate_after(node: Node) -> List[str]:
    commands = []

    for plugin in plugins:
        module = importlib.import_module(plugin)
        generator = getattr(module, 'generate_after')
        commands.extend(generator(node))

    return commands
