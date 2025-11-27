import uuid

class Node:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())
        self.active = True

class Graph:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.nodes = {}
        self.edges = {}

    def addNode(self, node):
        self.nodes[node.id] = node
        self.edges[node.id] = {}

    def deleteNode(self, node):
        self.nodes.pop(node.id, None)
        self.edges.pop(node.id, None)

    def addEdge(self, nodeIdA, nodeIdB, weight):
        self.edges[nodeIdA][nodeIdB] = weight
        self.edges[nodeIdB][nodeIdA] = weight
    
    def deleteEdge(self, nodeIdA, nodeIdB):
        self.edges[nodeIdA].discard(nodeIdB)
        self.edges[nodeIdB].discard(nodeIdA)