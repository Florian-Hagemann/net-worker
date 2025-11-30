import tkinter as tk
from tkinter import simpledialog, ttk, filedialog

class MainWindow:
    def findRoute(self):
        popup = tk.Toplevel(self.root)
        popup.title("Find Route")
        popup.geometry("300x250")

        # --- Start Node Selector ---
        tk.Label(popup, text="Start Node:").pack()
        startCombo = ttk.Combobox(popup, values=self.service.get_node_names())
        startCombo.pack()

        # --- Goal Node Selector ---
        tk.Label(popup, text="Goal Node:").pack()
        goalCombo = ttk.Combobox(popup, values=self.service.get_node_names())
        goalCombo.pack()

        # --- Weight Type Selector ---
        tk.Label(popup, text="Optimize by:").pack()
        weightCombo = ttk.Combobox(popup, values=["cost", "time", "distance"])
        weightCombo.set("cost")
        weightCombo.pack()

        # --- Button that runs Dijkstra ---
        def run():
            start_name = startCombo.get()
            goal_name = goalCombo.get()
            weight_type = weightCombo.get()

            startID = self.service.get_node_id(start_name)
            goalID = self.service.get_node_id(goal_name)

            if not startID or not goalID:
                tk.messagebox.showerror("Error", "Please choose valid nodes.")
                return

            path, dist, log = self.service.dijkstra_with_log(startID, goalID, weight_type)
            latex = self.service.dijkstra_log_to_latex(log, startID, goalID)

            # Show result in a new window
            result = tk.Toplevel(self.root)
            result.title("Route Result")
            result.geometry("700x600")

            # Path label
            tk.Label(result, text=f"Shortest path ({weight_type}):", font=("Arial", 12, "bold")).pack()

            path_names = " → ".join([self.service.getNodes()[nid].name for nid in path])
            tk.Label(result, text=path_names).pack()

            tk.Label(result, text=f"Total {weight_type}: {dist}").pack()

            # LaTeX box
            textBox = tk.Text(result, wrap="word")
            textBox.pack(fill="both", expand=True)
            textBox.insert("1.0", latex)

        tk.Button(popup, text="Calculate", command=run).pack(pady=10)
        tk.Button(popup, text="Close", command=popup.destroy).pack()

    def addEdge(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Edge")
        popup.geometry("250x150")

        destinationNodes = []
        for node in self.service.getNodes().values():
            if node.name != self.combo.get():
                destinationNodes.append(node.name)

        destinationNodeSelector = ttk.Combobox(popup, values=destinationNodes)
        destinationNodeSelector.pack()
        typeSelector = ttk.Combobox(popup, values=["ice", "regio"])
        typeSelector.pack()
        
        def positive_ints(new_value):
            if new_value == "":
                return True   # allow empty so user can type
            return new_value.isdigit() and new_value != "0"  # no zero if you want strictly positive

        vcmd = (popup.register(positive_ints), "%P")

        entry = tk.Entry(popup, validate="key", validatecommand=vcmd)
        entry.pack()

        def serviceCallAddEdge():
            self.service.addEdge(self.service.get_node_id(self.combo.get()), self.service.get_node_id(destinationNodeSelector.get()), int(entry.get()), typeSelector.get())
            self.updateEdgeTree()

        tk.Button(popup, text="Add", command=serviceCallAddEdge).pack()
        tk.Button(popup, text="Close", command=popup.destroy).pack()
  
    def updateEdgeTree(self, event=None):
        for item in self.edgeTree.get_children():
            self.edgeTree.delete(item)

        for edge in self.service.graph.edges[self.service.get_node_id(self.combo.get())]:
            self.edgeTree.insert("", tk.END, values=(self.service.getNodes()[edge].name, edge, self.service.graph.edges[self.service.get_node_id(self.combo.get())][edge]))
        
        self.edgeTree.pack(fill=tk.BOTH, expand=True)

    def updateNodeView(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for node in self.service.getNodes():
            self.tree.insert("", tk.END, values=(self.service.getNodes()[node].name, self.service.getNodes()[node].active, node))

        self.tree.pack(fill=tk.BOTH, expand=True)

    def addNode(self):
        nodeName = simpledialog.askstring("Add Node", "Enter node name: ")
        if nodeName == "" or nodeName == None:
            print("No name for node!")
            tk.Message(text="No name for node given!")
        else:
            self.service.addNode(nodeName)
            self.updateNodeView()

    def editEdges(self):
        popup = tk.Toplevel(self.root)
        popup.title("Edit Edges")
        popup.geometry("250x150")

        frameEdgeButtons = tk.Frame(popup)
        frameEdgeButtons.pack()

        tk.Label(frameEdgeButtons, text="Source Node: ").pack(side="left")

        self.combo = ttk.Combobox(frameEdgeButtons, values=self.service.get_node_names())
        self.combo.pack(side="left")
        self.combo.bind("<<ComboboxSelected>>", self.updateEdgeTree)

        tk.Button(frameEdgeButtons, text="Add Edge", command=self.addEdge).pack(side="left")

        self.edgeTree = ttk.Treeview(popup, show="headings")
        self.edgeTree["columns"] = ("Name", "ID", "Weight")
        self.edgeTree.heading("ID", text="Node ID")
        self.edgeTree.heading("Name", text="Node Name")
        self.edgeTree.heading("Weight", text="Weight")

        self.edgeTree.pack()

    def deleteNode(self):
        popup = tk.Toplevel(self.root)
        popup.title("Delete Node")
        popup.geometry("250x150")

        self.combo = ttk.Combobox(popup, values=self.service.get_node_names())
        self.combo.pack()

        def serviceCallDelete():
            self.service.deleteNode(self.service.get_node_id(self.combo.get()))
            self.updateNodeView()
            popup.destroy()

        tk.Button(popup, text="Delete", command=serviceCallDelete).pack()
        tk.Button(popup, text="Close", command=popup.destroy).pack()


    def editNodes(self):
        popup = tk.Toplevel(self.root)
        popup.title("Edit Nodes")
        popup.geometry("250x150")

        tree = ttk.Treeview(popup, columns=("ID"), show="headings")
        tree["columns"] = ("Name", "Active", "ID")
        tree.heading("ID", text="Node ID")
        tree.heading("Name", text="Node Name")
        tree.heading("Active", text="Active?")

        for node in self.service.getNodes():
            tree.insert("", tk.END, values=(self.service.getNodes()[node].name, self.service.getNodes()[node].active, node))

        tree.pack(fill=tk.BOTH, expand=True)
        tk.Button(popup, text="Delete Node", command=self.deleteNode).pack()
        tk.Button(popup, text="Close", command=popup.destroy).pack()

    def loadNetwork(self):
        # Open file dialog to choose a file
        file_path = filedialog.askopenfilename(
            title="Load Network",
            filetypes=(("Pickle files", "*.pkl"), ("All files", "*.*"))
        )
        if not file_path:
            return  # user canceled

        try:
            self.service.loadGraph(file_path)  # your service handles loading
            self.updateNodeView()
            if hasattr(self, "edgeTree"):
                self.updateEdgeTree()
            print(f"Network loaded from {file_path}")
        except Exception as e:
            print("Error loading network:", e)


    def saveGraph(self):
        file_path = filedialog.asksaveasfilename(
            title="Save file",
            defaultextension=".pkl",
            filetypes=(("Pickle files", "*.pkl"), ("All files", "*.*"))
        )

        if file_path:
            print("Save as:", file_path)
            self.service.saveGraph(file_path)

    def __init__(self, service):
        self.root = tk.Tk()
        self.root.title("net-worker")
        self.service = service

        title_label = tk.Label(
            self.root,
            text="Net-Worker",
            font=("Arial", 24, "bold")
        )
        title_label.pack(pady=10)

        # init frames
        self.frameButtons = tk.Frame(self.root)
        self.frameNodeView = tk.Frame(self.root)

        self.frameButtons.pack()
        self.frameNodeView.pack()

        self.tree = ttk.Treeview(self.frameNodeView, columns=("ID"), show="headings")
        self.tree["columns"] = ("Name", "Active", "ID")
        self.tree.heading("ID", text="Node ID")
        self.tree.heading("Name", text="Node Name")
        self.tree.heading("Active", text="Active?")
        self.updateNodeView()

        # add stuff to frames
        tk.Button(self.frameButtons, text="Load Network", command=self.loadNetwork).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Save Network", command=self.saveGraph).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Find Route", command=self.findRoute).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Add Node", command=self.addNode).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Edit Nodes", command=self.editNodes).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Edit Edges", command=self.editEdges).pack(pady=5, side="left")

    def start(self):
        self.root.mainloop();
