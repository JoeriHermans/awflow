from queue import Queue



class WorkflowGraph:

    def __init__(self):
        super(WorkflowGraph, self).__init__()
        self._roots = set([])
        self._nodes = {}

    def add(self, node):
        self._nodes[id(node.f)] = node

    def delete(self, node):
        del self._nodes[id(node.f)]

    def find(self, f):
        try:
            node = self._nodes[id(f)]
        except:
            node = None

        return node

    @property
    def nodes(self):
        return self._nodes.values()

    @property
    def roots(self):
        roots = []
        for node in self.nodes:
            if len(node.parents) == 0:
                roots.append(node)

        return roots

    @property
    def leaves(self):
        leaves = []
        for node in self.nodes:
            if len(node.children) == 0:
                leaves.append(node)

        return leaves
