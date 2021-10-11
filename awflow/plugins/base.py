import importlib

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node



plugins = [
    'awflow.plugins.chdir',
    'awflow.plugins.conda']



def apply_defaults(backend: str, workflow: DAWG, **kwargs):
    for plugin in plugins:
        module = importlib.import_module(plugin)
        applier = getattr(module, 'apply_defaults')
        for node in workflow.nodes:
            applier(backend, node, **kwargs)


def generate_before(backend: str, node: Node) -> list[str]:
    commands = []

    for plugin in plugins:
        module = importlib.import_module(plugin)
        generator = getattr(module, 'generate_before')
        commands.extend(generator(backend, node))

    return commands


def generate_after(backend: str, node: Node) -> list[str]:
    commands = []

    for plugin in plugins:
        module = importlib.import_module(plugin)
        generator = getattr(module, 'generate_after')
        commands.extend(generator(backend, node))

    return commands
