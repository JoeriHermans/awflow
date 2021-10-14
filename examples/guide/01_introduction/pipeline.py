r"""
This example familiarizes you with `awflow` and its
core functionality.

For every example, we'll explain the idea behind
the demonstration. Note that this particular file, every example is a
distinct workflow. Executing a workflow with
`aw.execute` will automatically clear the graph.
This can in principle be done manually using `aw.clear`.

The core concept in `awflow` is the notion of a task.
Essentially, this is a method that will be executed in your workflow.
Tasks represented as a node in a directed graph. In doing so,
we can easily specify dependencies. In addition, we can attribute
properties to tasks using Python decorators.
"""

import awflow as aw



################################################################################
# Example 1
################################################################################
r"""
In this example we show that certain requirements need to be met in order for
tasks to be incorporated into the compute graph. Simply specifying this method
and calling `aw.execute` will obviously do nothing. Since the module cannot know
whether `example1_main` is a node in the compute graph, or simply an
utility function.
"""

def example1_main():
    print("This message will not be shown!")

# Execute the workflow
aw.execute()  # Nothing will happen as `example1_main` is not incorporated in the graph.


################################################################################
# Example 2
################################################################################
r"""
If you don't specify any other task decorator, but you would like to
incorporate the task into the compute graph, you can simply tag the
method with the `node` decorator.
"""


@aw.node  # Forces the addition of a node to the workflow graph.
def example2_main():
    print("This method will be executed!")

# Execute the workflow
aw.execute()


r"""
However, if your method has certain requirements, such as a
certain number of CPU cores, specifying `aw.node` is not necessary.
Since it will be handled automatically. For instance
"""
@aw.cpus(4)  # Requests 4 CPU cores when executing this method.
def example2_demonstration():
    print("This method will be executed!")

# Execute the workflow
aw.execute()


################################################################################
# Example 3
################################################################################
r"""
However, if your workflow does have tasks with certain dependencies
, specifying the `@aw.node` decorator is not necessary.
"""

def example3_main():
    print("This does something.")

@aw.dependency(example3_main)
def example3_dependency():
    print("This will be executed only after `example3_main`.")

# Execute the workflow.
aw.execute()
