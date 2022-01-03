class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class Frontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        """Append a node to the frontier"""
        self.frontier.append(node)

    def contains_state(self, state):
        """
        Check whether the frontier contains a 
        node with a specific state.
        """
        return any(node.state == state for node in self.frontier)

    def empty(self):
        """Check if the lenght of the frontier is zero""" 
        return len(self.frontier) == 0

    def remove(self):
        """
        Remove a node from the frontier
        Needs to be implemented.
        """
        raise NotImplementedError

class StackFrontier(Frontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(Frontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
