import tkinter as tk
from tkinter import simpledialog, ttk

class MainWindow:

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

        combo = ttk.Combobox(popup, values=self.service.get_node_names())
        combo.pack()

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
        tk.Button(popup, text="Close", command=popup.destroy).pack()

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
        tk.Button(self.frameButtons, text="Load Network", command=service.placeholder).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Save Network", command=service.placeholder).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Find Route", command=service.placeholder).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Add Node", command=self.addNode).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Edit Nodes", command=self.editNodes).pack(pady=5, side="left")
        tk.Button(self.frameButtons, text="Edit Edges", command=self.editEdges).pack(pady=5, side="left")

    def start(self):
        self.root.mainloop();
