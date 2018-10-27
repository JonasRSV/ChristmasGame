from geventwebsocket.exceptions import WebSocketError
from overrides import overrides
import facts


class FactsImpl(facts.Facts):
    @overrides
    def on_open(self) -> None:
        try:
            self.ws.send("Hello")
        except WebSocketError as e:
            self.state.logger.error("WebsocketError - Cause: {}".format(
                str(e)))

    @overrides
    def on_message(self, message) -> None:
        try:
            self.ws.send("I Recieved {}".format(message))
        except WebSocketError as e:
            self.state.logger.error("WebsocketError - Cause: {}".format(
                str(e)))

    @overrides
    def on_close(self, reason: str) -> None:
        self.state.logger.info("Facts connection closed - Cause: {}".format(
            str(e)))
