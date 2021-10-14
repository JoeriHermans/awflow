r"""
This example familiarizes you with `awflow` and its
core functionality.
"""

import awflow as aw



################################################################################
# Example 1
################################################################################
r"""
TODO
"""

def example1_main():
    print("This message will not be shown!")

# Execute the workflow
aw.execute()


################################################################################
# Example 2
################################################################################
r"""
TODO
"""


@aw.node  # Forces the addition of a node to the workflow graph.
def example2_main():
    print("This does method will get executed!")

# Execute the workflow
aw.execute()


################################################################################
# Example 3
################################################################################
r"""
However, if your workflow does have tasks with certain dependencies for whatever
reason, specifying the `@aw.node` decorator is not necessary.
"""

def example3_main():
    print("This does something.")

@aw.dependency(example3_main)
def example3_dependency():
    print("This will be executed only after `example3_main`.")

aw.execute()
