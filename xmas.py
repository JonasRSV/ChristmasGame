import impl.client
import threading
import time
from geventwebsocket import WebSocketServer, Resource
from collections import OrderedDict
from app_state import State
from app_gui import Gui


if __name__ == "__main__":
    xmas = WebSocketServer(('0.0.0.0', 8000),
                        Resource(OrderedDict([('/',
                                               impl.client.ClientImpl)])))

    application_state = State()
    application_gui = Gui(application_state)
    xmas.state = application_state

    try: 
        application_gui.start()
        xmas.start()
        xmas.serve_forever()
    except KeyboardInterrupt:
        pass

    application_state.clean()
    application_gui.stop()
