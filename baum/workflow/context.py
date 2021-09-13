from baum.workflow import WorkflowGraph



class WorkflowContext:

    def __init__(self):
        super(WorkflowContext, self).__init__()
        self._graph = WorkflowGraph()

    @property
    def graph(self):
        return self._graph

    def find(self, f):
        return self.graph.find(f)
