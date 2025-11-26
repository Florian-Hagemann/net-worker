from .gui import MainWindow
from .core import Service

class Application:
    def __init__(self):
        self.service = Service()
        self.window = MainWindow(self.service)

    def run(self):
        self.window.start()