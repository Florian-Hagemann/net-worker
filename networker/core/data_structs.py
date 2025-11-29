import uuid

class Edge:
    def __init__(self, distance, routetype):
        self.distance = float(distance)
        self.type = routetype
        
        if self.type == "ice":
            self.cost = 0.15 * self.distance
            self.time = self.distance / 150
        else:
            self.cost = 0.07 * self.distance
            self.time = self.distance / 90
        
        print(f"Created Edge \n Distance: {self.distance} \n Type: {self.type} \n Cost: {self.cost} \n Time: {self.time}")


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

    def addEdge(self, nodeIdA, nodeIdB, weight, routetype):
        edge = Edge(weight, routetype)
        self.edges[nodeIdA][nodeIdB] = edge
        self.edges[nodeIdB][nodeIdA] = edge
    
    def deleteEdge(self, nodeIdA, nodeIdB):
        self.edges[nodeIdA].discard(nodeIdB)
        self.edges[nodeIdB].discard(nodeIdA)