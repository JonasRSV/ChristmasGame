from geventwebsocket.exceptions import WebSocketError
from overrides import overrides
from collections import Counter
import interface
import json
import math


class InterfaceImpl(interface.Interface):
    def __get_message(self) -> str:
        combinations = math.factorial(len(self.state.packages))
        for occurrence in Counter(self.state.packages).values():
            combinations = combinations / math.factorial(occurrence)

        response = {
            "packages": len(self.state.packages),
            "combinations": int(combinations)
        }

        return json.dumps(response)

    @overrides
    def on_open(self) -> None:
        try:
            self.ws.send(self.__get_message())
        except WebSocketError as e:
            self.state.logger.error("WebsocketError - Cause: {}".format(
                str(e)))

    @overrides
    def on_message(self, message) -> None:
        self.state.add_package(message)
        try:
            message = self.__get_message()
            for client in self.ws.handler.server.clients.values():
                client.ws.send(message)
        except WebSocketError as e:
            self.state.logger.error("WebsocketError - Cause: {}".format(
                str(e)))

    @overrides
    def on_close(self, reason: str) -> None:
        self.state.logger.info(
            "Interface connection closed - Cause: {}".format(str(reason)))
