import tkinter as tk

class MainWindow:
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

    
    def start(self):
        self.root.mainloop();
