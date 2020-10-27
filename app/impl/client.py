from geventwebsocket.exceptions import WebSocketError
from overrides import overrides
import client


class ClientImpl(client.Client):
    @overrides
    def on_message(self, message) -> None:
        try:
            self.ws.send(self.state.package)
        except WebSocketError as e:
            self.state.logger.error("WebsocketError, probably dead connection: {}".format(
                str(e)))
