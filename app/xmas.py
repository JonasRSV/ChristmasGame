import impl.client as client
import impl.interface as interface
import impl.santa as santa
import impl.gui as gui
from geventwebsocket import WebSocketServer, Resource
from collections import OrderedDict
from app_state import State


def main():
    xmas = WebSocketServer(('0.0.0.0', 8000),
                           Resource(
                               OrderedDict([('/xmas', client.ClientImpl),
                                            ('/interface',
                                             interface.InterfaceImpl)])))

    application_state = State()
    application_gui = gui.GuiImpl(application_state,
                                  santa.GaOptimizingSanta(application_state))
    """ So that interface can update the packages aswell. """
    application_state.add_package = application_gui.add_package
    """ Make state reachable throughout all applications """
    xmas.state = application_state

    try:
        application_gui.start()
        xmas.start()
        xmas.serve_forever()
    except KeyboardInterrupt:
        pass

    application_state.clean()
    application_gui.stop()


if __name__ == "__main__":
    main()
