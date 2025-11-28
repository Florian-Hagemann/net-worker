import pickle
from .data_structs import Graph, Node

class Service:
    def __init__(self):
        self.graph = Graph()
    
    def addNode(self, nodeName):
        node = Node(nodeName)
        print(f"Added {nodeName} with the ID {node.id}")
        self.graph.addNode(node)
    
    def addEdge(self, nodeA, nodeB, weight):
        self.graph.addEdge(nodeA, nodeB, weight)
        print(f"Edge added between {nodeA} and {nodeB} with weight = {weight}")
    
    def get_node_names(self):
        return [node.name for node in self.graph.nodes.values()]

    def get_node_id(self, name):
        for nid, node in self.graph.nodes.items():
            if node.name == name:
                return nid
        
        return None

    def getNodes(self):
        return self.graph.nodes

    def saveGraph(self, file):
        with open(file, "wb") as f:
            pickle.dump(self.graph, f)

    def loadGraph(self, file):

        with open(file, "rb") as f:
            self.graph = pickle.load(f)

    def placeholder(self):
        print("hello world!")