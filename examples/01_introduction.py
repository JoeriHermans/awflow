import baum as b


def graph1():
    print("This is the first graph")


@b.dependency(graph1)
def dependency_of_graph1():
    print("Dependency of graph1.")


def graph2():
    print("This is the second graph")


@b.dependency(graph2)
def dependency_of_graph2():
    print("Dependency of graph2.")
