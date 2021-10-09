import awflow as aw

from awflow import workflow



def graph1():
    print("This is the first graph")


@aw.dependency(graph1)
def dependency_of_graph1():
    print("Dependency of graph1.")


def graph2():
    print("This is the second graph")


@aw.dependency(graph2)
def dependency_of_graph2():
    print("Dependency of graph2.")
