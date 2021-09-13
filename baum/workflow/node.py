class WorkflowNode:

    def __init__(self, f):
        super(WorkflowNode, self).__init__()
        self.f = f
        self._attributes = {}
        self._children = []
        self._disabled = False
        self._parents = []
        self._postconditions = []
        self._tasks = 1

    @property
    def attributes(self):
        return self._attributes

    @property
    def postconditions(self):
        return self._postconditions

    def add_postcondition(self, condition):
        self._postconditions.append(condition)

    def has_posconditions(self):
        return len(self.postconditions) > 0

    def postconditions_satisfied(self):
        return all(c() for c in self.postconditions)

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, value):
        assert value >= 1
        self._tasks = value

    @property
    def name(self):
        if "name" in self._attributes.keys():
            return self._attributes["name"]
        else:
            return self.f.__name__

    @name.setter
    def name(self, value):
        self._attributes["name"] = value

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, state):
        self._disabled = state

    def __setitem__(self, key, value):
        self._attributes[key] = value

    def __getitem__(self, key):
        return self._attributes[key]

    @property
    def parents(self):
        return self._parents

    @parents.setter
    def parents(self, parents):
        self._parents = parents

    def add_parent(self, node):
        assert node is not None
        self._parents.append(node)
        node._children.append(self)
        node._children = list(set(node._children))
        self._parents = list(set(self._parents))

    def remove_parent(self, node):
        if node in self._parents:
            index = self._parents.index(node)
            del self._parents[index]
        if self in node.children:
            node.remove_child(self)

    def add_child(self, node):
        assert node is not None
        self._children.append(node)
        node._parents.append(self)
        self._children = list(set(self._children))
        node._parents = list(set(node._parents))

    def remove_child(self, node):
        if node in self._children:
            index = self._children.index(node)
            del self._children[index]
        if self in node.parents:
            node.remove_parent(self)

    @property
    def dependencies(self):
        return self.parents

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children

    def __del__(self):
        for p in self.parents:
            p.remove_child(self)
        for c in self.children:
            c.remove_parent(self)

    def __str__(self):
        return self.name
