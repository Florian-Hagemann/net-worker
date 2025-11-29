import pickle
from .data_structs import Graph, Node
import math

class Service:
    def __init__(self):
        self.graph = Graph()
    
    def dijkstra_log_to_latex(self, log, decimal_places=2):
        node_ids = list(self.graph.nodes.keys())

        latex = []

        latex.append("\\begin{table}[h!]")
        latex.append("\\centering")
        latex.append("\\begin{tabular}{|c|c|" +
                    " ".join(["c" for _ in node_ids]) +
                    "|c|}")
        latex.append("\\hline")

        # Tabellenkopf
        header = ["\\textbf{Iter.}", "\\textbf{Aktueller Knoten}"]
        header += [f"\\textbf{{{self.graph.nodes[n].name}}}" for n in node_ids]
        header += ["\\textbf{Vorgänger}"]
        latex.append(" & ".join(header) + " \\\\ \\hline")

        # Jede Iteration einfügen
        for entry in log:
            row = []

            row.append(str(entry["iteration"]))  # Iteration
            row.append(self.graph.nodes[entry["current"]].name
                    if entry["current"] else "--")  # Current Node

            # Distanzspalten with rounding
            for nid in node_ids:
                d = entry["distances"][nid]
                if d == float("inf"):
                    row.append("$\\infty$")
                else:
                    # Round the value to `decimal_places` decimal places
                    rounded_distance = round(d, decimal_places)
                    row.append(f"${rounded_distance}$")  # Distance

            # Vorgängerspalte
            prev_list = []
            for nid in node_ids:
                p = entry["previous"][nid]
                if p is None:
                    prev_list.append(f"{self.graph.nodes[nid].name}: --")
                else:
                    prev_list.append(
                        f"{self.graph.nodes[nid].name}: {self.graph.nodes[p].name}"
                    )
            row.append(", ".join(prev_list))  # Predecessors

            latex.append(" & ".join(row) + " \\\\ \\hline")

        latex.append("\\end{tabular}")
        latex.append("\\caption{Dijkstra-Distanzentabelle}")
        latex.append("\\end{table}")

        return "\n".join(latex)



    def dijkstra_with_log(self, start, goal, weight_type):
        import heapq
    
        distances = {node: float("inf") for node in self.graph.nodes}
        previous = {node: None for node in self.graph.nodes}
        distances[start] = 0
    
        pq = [(0, start)]
        log = []
        iteration = 0  # Add iteration counter
    
        while pq:
            current_distance, current = heapq.heappop(pq)
    
            if current == goal:
                break
            
            for neighbor, edge in self.graph.edges[current].items():
                # Use correct attribute from Edge based on GUI selection
                weight = getattr(edge, weight_type)
                alt = current_distance + weight
    
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current
                    heapq.heappush(pq, (alt, neighbor))
    
                    # Log as a dictionary instead of a string, with rounding applied to distances
                    log.append({
                        "iteration": iteration,
                        "current": current,
                        "distances": {nid: round(distances[nid], 2) for nid in distances},  # Round distances here
                        "previous": previous.copy(),  # Store the current state of previous nodes
                    })
    
            iteration += 1  # Increment iteration count
    
        path = []
        cur = goal
        while cur is not None:
            path.append(cur)
            cur = previous[cur]
    
        path.reverse()
        return path, distances[goal], log
    




                    
        

    def addNode(self, nodeName):
        node = Node(nodeName)
        print(f"Added {nodeName} with the ID {node.id}")
        self.graph.addNode(node)
    
    def deleteNode(self, nodeId):
        print(f"Delete node {nodeId}")
        self.graph.deleteNode(self.graph.nodes[nodeId])

    def addEdge(self, nodeA, nodeB, weight, routetype):
        self.graph.addEdge(nodeA, nodeB, weight, routetype)
        print(f"Edge added between {nodeA} and {nodeB}")
    
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