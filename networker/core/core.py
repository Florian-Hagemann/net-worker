import pickle
from .data_structs import Graph, Node
import math

class Service:
    def __init__(self):
        self.graph = Graph()

    # ---------- Utility: escape latex special characters ----------
    def _escape_latex(self, s):
        if s is None:
            return ""
        return (
            s.replace("\\", r"\textbackslash ")
             .replace("_", r"\_")
             .replace("%", r"\%")
             .replace("&", r"\&")
             .replace("#", r"\#")
             .replace("{", r"\{")
             .replace("}", r"\}")
        )

    # ---------------------------------------------------------------
    def dijkstra_with_log(self, start, goal, weight_type):
        import heapq

        distances = {node: float("inf") for node in self.graph.nodes}
        previous = {node: None for node in self.graph.nodes}
        distances[start] = 0

        pq = [(0, start)]
        log = []
        iteration = 0

        while pq:
            current_distance, current = heapq.heappop(pq)

            # stale queue entries
            if current_distance > distances[current]:
                continue

            updates = []

            # Goal reached → stop (Dijkstra valid for non-negative weights)
            if current == goal:
                log.append({
                    "iteration": iteration,
                    "current": current,
                    "distances": distances.copy(),
                    "previous": previous.copy(),
                    "updated": updates
                })
                break

            # Relax edges safely
            for neighbor, edge in self.graph.edges.get(current, {}).items():
                weight = getattr(edge, weight_type, None)
                if weight is None:
                    raise ValueError(f"Edge between {current} and {neighbor} missing weight type '{weight_type}'")

                alt = current_distance + weight
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current
                    heapq.heappush(pq, (alt, neighbor))
                    updates.append(neighbor)

            log.append({
                "iteration": iteration,
                "current": current,
                "distances": distances.copy(),
                "previous": previous.copy(),
                "updated": updates
            })

            iteration += 1

        # ------ Reconstruct path safely ------
        path = []
        cur = goal
        visited_nodes = set()  # prevent infinite loops

        while cur is not None and cur not in visited_nodes:
            visited_nodes.add(cur)
            path.append(cur)
            cur = previous.get(cur, None)

        path.reverse()

        return path, distances[goal], log

    # ---------------------------------------------------------------
    def dijkstra_log_to_latex(self, log, start, goal, decimal_places=2):
        """
        Generate LaTeX table from log.
        Incorporates fixes: makecell, escaping, safe access, stable ordering.
        """
        from math import inf

        # ---- STABLE column order ----
        node_ids = sorted(self.graph.nodes.keys())
        node_names = [self._escape_latex(self.graph.nodes[n].name) for n in node_ids]

        latex = []
        latex.append("\\begin{table}[h!]")
        latex.append("\\centering")
        latex.append("\\renewcommand{\\arraystretch}{1.4}")
        latex.append("% Requires: colortbl, xcolor, multirow, makecell packages")
        latex.append("\\definecolor{visited}{RGB}{153,255,153}")   # green
        latex.append("\\definecolor{updated}{RGB}{255,204,204}")   # pink
        latex.append("\\definecolor{goalred}{RGB}{255,102,102}")   # red

        columns = "|c|c|" + "|".join(["c" for _ in node_ids]) + "|"
        latex.append(f"\\begin{{tabular}}{{{columns}}}")
        latex.append("\\hline")

        header = ["\\textbf{Iter}", "\\textbf{Besucht}"]
        header += [f"\\textbf{{{name}}}" for name in node_names]
        latex.append(" & ".join(header) + " \\\\ \\hline")

        for entry in log:
            iteration = entry["iteration"]
            current = entry.get("current", None)
            distances = entry.get("distances", {})
            previous = entry.get("previous", {})
            updated = entry.get("updated", [])

            row = []

            # Iteration column
            row.append(str(iteration))

            # ---------------- Visited column ----------------
            if current is None:
                row.append("{--}")
            else:
                node_name = self._escape_latex(self.graph.nodes[current].name)
                d = distances.get(current, inf)

                # format distance
                if d == inf:
                    dist_str = r"$\infty$"
                else:
                    dist_str = f"{int(round(d))}" if decimal_places == 0 else f"{d:.{decimal_places}f}"

                # multiline → wrapped in makecell
                visited_content = f"\\makecell{{\\textbf{{{node_name}}} \\\\ d={dist_str}}}"

                color = "goalred" if current == goal else "visited"
                row.append(f"\\cellcolor{{{color}}}{{{visited_content}}}")

            # ---------------- Distance columns ----------------
            for nid in node_ids:
                d = distances.get(nid, inf)
                pred = previous.get(nid, None)
                pred_name = self._escape_latex(self.graph.nodes[pred].name) if pred in self.graph.nodes else None

                # Content
                if d == inf:
                    cell_content = r"$\infty$"
                else:
                    dist_str = f"{int(round(d))}" if decimal_places == 0 else f"{d:.{decimal_places}f}"
                    if pred_name:
                        cell_content = f"\\makecell{{{dist_str} \\\\ ({pred_name})}}"
                    else:
                        cell_content = f"{dist_str}"

                # Coloring logic
                color = None
                if nid == current:
                    color = "visited"
                if (nid in updated) and (current != goal):
                    color = "updated"
                if (current == goal) and (nid == goal):
                    color = "goalred"

                if color:
                    row.append(f"\\cellcolor{{{color}}}{{{cell_content}}}")
                else:
                    row.append(f"{{{cell_content}}}")

            latex.append(" & ".join(row) + " \\\\ \\hline")

        latex.append("\\end{tabular}")
        latex.append("\\caption{Dijkstra-Distanzentabelle}")
        latex.append("\\end{table}")

        return "\n".join(latex)

    # ---------------------------------------------------------------
    def addNode(self, nodeName):
        node = Node(nodeName)
        print(f"Added {nodeName} with the ID {node.id}")
        self.graph.addNode(node)

    def deleteNode(self, nodeId):
        if nodeId not in self.graph.nodes:
            raise ValueError(f"Node {nodeId} does not exist")
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
