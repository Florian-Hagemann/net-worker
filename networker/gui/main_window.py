import tkinter as tk
from tkinter import simpledialog, ttk

class MainWindow:

    def addNode(self):
        nodeName = simpledialog.askstring("Add Node", "Enter node name: ")
        self.service.addNode(nodeName)

    def editNodes(self):
        popup = tk.Toplevel(self.root)
        popup.title("Edit Nodes")
        popup.geometry("250x150")

        tree = ttk.Treeview(popup, columns=("ID"), show="headings")
        tree["columns"] = ("Name", "ID")
        tree.heading("ID", text="Node ID")
        tree.heading("Name", text="Node Name")

        for node in self.service.getNodes():
            tree.insert("", tk.END, values=(self.service.getNodes()[node].name, node))

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
        self.frameGraph = tk.Frame(self.root)

        self.frameButtons.pack()

        # add stuff to frames
        tk.Button(self.frameButtons, text="Load Network", command=service.placeholder).pack()
        tk.Button(self.frameButtons, text="Save Network", command=service.placeholder).pack()
        tk.Button(self.frameButtons, text="Find Route", command=service.placeholder).pack()
        tk.Button(self.frameButtons, text="Add Node", command=self.addNode).pack()
        tk.Button(self.frameButtons, text="Edit Nodes", command=self.editNodes).pack()
    
    def start(self):
        self.root.mainloop();
