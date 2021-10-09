import importlib

from awflow.dawg import DirectedAcyclicWorkflowGraph as DAWG
from awflow.node import Node



plugins = [
    'awflow.plugins.conda']



def apply_defaults(workflow: DAWG, **kwargs):
    for plugin in plugins:
        module = importlib.import_module(plugin)
        applier = getattr(module, 'apply_defaults')
        for node in workflow.nodes:
            applier(node)


def generate(node: Node) -> list[str]:
    commands = []

    for plugin in plugins:
        module = importlib.import_module(plugin)
        generator = getattr(module, 'generate')
        commands.extend(generator(node))

    return commands
