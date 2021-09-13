import baum as b

from baum.util import is_iterable
from baum.workflow.util import add_and_get_node
from baum.workflow.util import parameterized


def root(f):
    node = add_and_get_node(f)
    b.context.graph.add_root(node)

    return f


@parameterized
def dependency(f, dependencies):
    if not is_iterable(dependencies):
        dependencies = [dependencies]
    for dependency in dependencies:
        if f == dependency:
            raise Exception("A function cannot depend on itself.")
        dependency_node = add_and_get_node(dependency)
        node = add_and_get_node(f)
        node.add_parent(dependency_node)

    return f
