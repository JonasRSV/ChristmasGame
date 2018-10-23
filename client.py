import copy
from abc import abstractmethod
from geventwebsocket import WebSocketApplication


class Client(WebSocketApplication):
    def __init__(self, *args):
        WebSocketApplication.__init__(self, *args)
        self.state = self.ws.handler.server.state

    def on_open(self) -> None:
        self.state.logger.info(" -- Recieved Connection -- ")

        for IP, ID in self.ws.handler.server.clients.keys():
            self.state.logger.info(
                "Active Connection - IP: {} - ID: {}".format(IP, ID))

        self.ws.send(self.state.package)

    @abstractmethod
    def on_message(self, message) -> None:
        pass

    def on_close(self, reason: str) -> None:
        self.state.logger.info(" -- Closed Connection -- ")

        for IP, ID in self.ws.handler.server.clients.keys():
            self.state.logger.info(
                "Active Connection - IP: {} - ID: {}".format(IP, ID))
