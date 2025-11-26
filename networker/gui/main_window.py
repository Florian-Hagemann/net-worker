import tkinter as tk

class MainWindow:
    def __init__(self, service):
        self.root = tk.Tk()
        self.root.title("net-worker")
        self.service = service

        tk.Label(text="kill me please").pack()
    
    def start(self):
        self.root.mainloop();
