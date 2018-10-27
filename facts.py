from abc import abstractmethod
from geventwebsocket import WebSocketApplication


class Facts(WebSocketApplication):
    def __init__(self, *args):
        WebSocketApplication.__init__(self, *args)
        self.state = self.ws.handler.server.state

    @abstractmethod
    def on_open(self) -> None:
        pass

    @abstractmethod
    def on_message(self, message) -> None:
        pass

    @abstractmethod
    def on_close(self, reason: str) -> None:
        pass
