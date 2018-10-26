import threading
from abc import abstractmethod


class Gui(threading.Thread):

    def __init__(self, state: "State", santa: "Santa"):
        threading.Thread.__init__(self)
        self.state = state
        self.santa = santa

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def run(self):
        pass

