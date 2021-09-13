import baum as b

from baum.workflow import WorkflowContext
from baum.workflow import WorkflowGraph
from baum.workflow import WorkflowNode


def parameterized(dec):
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer


def add_and_get_node(f):
    if b.context is None:
        b.context = WorkflowContext()
    node = b.context.find(f)
    if node is None:
        node = WorkflowNode(f)
        b.context.graph.add(node)

    return node
