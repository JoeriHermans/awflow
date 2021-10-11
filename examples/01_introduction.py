import awflow as aw
import os

from awflow import workflow



def graph1():
    print(os.getcwd())
    print("This is the first graph")


@aw.dependency(graph1)
def dependency_of_graph1():
    print(os.getcwd())
    print("Dependency of graph1.")


def graph2():
    print(os.getcwd())
    print("This is the second graph")


@aw.dependency(graph2)
@aw.name("A different name")
@aw.chdir('/home/joeri/Downloads')
def dependency_of_graph2():
    print(os.getcwd())
    print("Dependency of graph2.")


@aw.dependency([dependency_of_graph1, dependency_of_graph2])
@aw.tasks(2)
def dependency_of_both_graphs(task_index):
    print(os.getcwd())
    print("Only after both subgraphs are done.")
    print(task_index)


aw.execute(backend='slurm', chdir='/home/joeri')
