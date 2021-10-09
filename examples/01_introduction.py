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
@aw.name("A different name")
def dependency_of_graph2():
    print("Dependency of graph2.")


@aw.dependency([dependency_of_graph1, dependency_of_graph2])
@aw.tasks(10)
def dependency_of_both_graphs(task_index):
    print("Only after both subgraphs are done.")
    print(task_index)


aw.execute(backend='standalone', generate_code=True)
