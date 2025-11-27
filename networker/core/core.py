from .loader import *
from .data_structs import Graph, Node

class Service:
    def __init__(self):
        self.graph = Graph()
    
    def addNode(self, nodeName):
        node = Node(nodeName)
        print(f"Added {nodeName} with the ID {node.id}")
        self.graph.addNode(node)
    
    def get_node_names(self):
        return [node.name for node in self.graph.nodes.values()]

    def get_node_id(self, name):
        for nid, node in self.graph.nodes.items():
            if node.name == name:
                return nid
        
        return None

    def getNodes(self):
        return self.graph.nodes

    def placeholder(self):
        print("hello world!")