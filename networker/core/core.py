from .loader import *
from .data_structs import Graph, Node

class Service:
    def __init__(self):
        self.graph = Graph()
    
    def addNode(self, nodeName):
        node = Node(nodeName)
        print(f"Added {nodeName} with the ID {node.id}")
        self.graph.addNode(node)

    def getNodes(self):
        return self.graph.nodes

    def placeholder(self):
        print("hello world!")