import impl.client as client
import impl.heap_santa as santa
import impl.gui as gui
import threading
import time
from geventwebsocket import WebSocketServer, Resource
from collections import OrderedDict
from app_state import State

if __name__ == "__main__":
    xmas = WebSocketServer(('0.0.0.0', 8000),
                           Resource(OrderedDict([('/', client.ClientImpl)])))

    application_state = State()
    application_gui = gui.GuiImpl(application_state,
                                  santa.SantaImpl(application_state))

    xmas.state = application_state

    try:
        application_gui.start()
        xmas.start()
        xmas.serve_forever()
    except KeyboardInterrupt:
        pass

    application_state.clean()
    application_gui.stop()
