import awflow as aw
import os


def graph1():
    print(os.getcwd())
    print("This is the first graph")


@aw.dependency(graph1)
def dependency_of_graph1():
    print(os.getcwd())
    print("Dependency of graph1.")


@aw.disable
def graph2():
    print("This is not executed!")


@aw.dependency(graph2)
@aw.name("A different name")
def dependency_of_graph2():
    print(os.getcwd())
    print("Dependency of graph2.")


@aw.dependency([dependency_of_graph1, dependency_of_graph2])
@aw.disable
@aw.tasks(2)
def dependency_of_both_graphs(task_index):
    print("This is not executed!")


if __name__ == '__main__':
    aw.execute()
