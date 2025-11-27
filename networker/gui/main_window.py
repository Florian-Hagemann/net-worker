import tkinter as tk
from tkinter import simpledialog

class MainWindow:

    def addNode(self):
        nodeName = simpledialog.askstring("Add Node", "Enter node name: ")
        self.service.addNode(nodeName)

    def __init__(self, service):
        self.root = tk.Tk()
        self.root.title("net-worker")
        self.service = service

        # init frames
        self.frameButtons = tk.Frame(self.root)
        self.frameGraph = tk.Frame(self.root)

        self.frameButtons.pack()

        # add stuff to frames
        tk.Button(self.frameButtons, text="Load Network", command=service.placeholder).pack()
        tk.Button(self.frameButtons, text="Save Network", command=service.placeholder).pack()
        tk.Button(self.frameButtons, text="Find Route", command=service.placeholder).pack()
        tk.Button(self.frameButtons, text="Add Node", command=self.addNode).pack()
        tk.Button(self.frameButtons, text="Edit Nodes", command=service.placeholder).pack()
    
    def start(self):
        self.root.mainloop();
