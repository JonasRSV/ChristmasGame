import threading
import time
import curses
from curses.textpad import Textbox


class Gui(threading.Thread):
    def __init__(self, state):
        self.state = state
        self.packages = []
        self.package_index = 0
        threading.Thread.__init__(self)

        self.display_window = None
        self.input_window = None
        self.textbox_win = None
        self.stdscr = None
        self.display_max = 200
        self.running = False

    def __display_packages(self) -> None:
        width_shift = 1
        for index, package in enumerate(
                reversed(self.packages[:self.package_index])):
            if index > self.display_max:
                break

            if index % 50 == 0 and index > 0:
                width_shift += 4

            self.display_window.addstr(
                ((index % 50) + 1) * int(curses.LINES / 30),
                (width_shift) * int(curses.COLS / 30), "{} - {}".format(
                    index, package), curses.A_BOLD)

        self.display_window.refresh()

    def __initialize_screen(self) -> None:
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        self.input_window = curses.newwin(curses.LINES, int(curses.COLS / 2),
                                          0, 0)
        self.display_window = curses.newwin(curses.LINES, int(curses.COLS / 2),
                                            0, int(curses.COLS / 2))

        self.textbox_win = self.input_window.subwin(
            30, 60, 9 * int(curses.LINES / 30), 2 * int(curses.COLS / 30))

        self.display_window.border()

        self.__paint_information_header()

        self.display_window.refresh()
        self.input_window.refresh()

    def __paint_information_header(self) -> None:
        self.input_window.border()
        self.input_window.addstr(
            int(curses.LINES / 30), int(curses.COLS / 30),
            "Add [a] - Remove [r] - Next [n] - Previous Package [p] - Sort [s]",
            curses.A_UNDERLINE)

    def __clean_screen(self) -> None:
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        self.running = False

    def __pick_indicator(self, text: str) -> None:
        self.input_window.addstr(4 * int(curses.LINES / 30),
                                 1 * int(curses.COLS / 30), "Mode: ",
                                 curses.A_BOLD)

        self.input_window.addstr(4 * int(curses.LINES / 30),
                                 2 * int(curses.COLS / 30), text,
                                 curses.A_STANDOUT)
        self.input_window.refresh()

    def __information(self, text: str) -> None:
        self.input_window.addstr(3 * int(curses.LINES / 30),
                                 1 * int(curses.COLS / 30),
                                 "Information: {}".format(text), curses.A_BOLD)
        self.input_window.refresh()

    def __textbox_input(self):
        self.input_window.addstr(
            7 * int(curses.LINES / 30), 2 * int(curses.COLS / 30),
            "Use newline as separator - Press CTRL-G to Submit", curses.A_BOLD)

        box = Textbox(self.textbox_win)

        self.input_window.refresh()
        self.textbox_win.refresh()

        box.edit()

        message = box.gather()

        self.textbox_win.clear()
        self.input_window.clear()

        self.__paint_information_header()
        self.input_window.refresh()

        return message

    def __add_packages(self):
        self.display_window.clear()
        self.display_window.border()
        self.__pick_indicator("a")
        self.__information("Input the name of packages to add")

        for package in self.__textbox_input().split("\n"):
            package = package.strip()

            if len(package) > 0:
                self.packages.append(package)

        self.package_index = len(self.packages)
        self.__display_packages()
        self.__information("Add successful")

    def __remove_packages(self):
        self.display_window.clear()
        self.display_window.border()
        self.__pick_indicator("r")
        self.__information("Input the index of packages to remove")

        for package_index in self.__textbox_input().split("\n"):
            index = None
            try:
                index = int(package_index.strip())
            except ValueError:
                continue

            absolute_index = self.package_index - index - 1

            if absolute_index >= 0 and absolute_index < self.package_index:
                del self.packages[absolute_index]

        packages = []
        for package in self.packages:
            if package is not None:
                packages.append(package)

        self.packages = packages
        self.package_index = min(self.package_index, len(self.packages))

        self.__display_packages()
        self.__information("Removed successful")

    def __next_package(self) -> None:
        self.display_window.clear()
        self.display_window.border()
        self.__pick_indicator("n")
        self.package_index -= 1

        if self.package_index < 0:
            self.package_index = 0

        self.__display_packages()
        self.__update_package_server()

    def __previous_package(self) -> None:
        self.display_window.clear()
        self.display_window.border()
        self.__pick_indicator("p")
        self.package_index += 1

        if self.package_index > len(self.packages):
            self.package_index = len(self.packages)

        print(self.package_index)
        self.__display_packages()
        self.__update_package_server()

    def __get_option(self) -> str:
        return chr(
            self.input_window.getch(10 * int(curses.LINES / 30),
                                    9 * int(curses.COLS / 30)))

    def __update_package_server(self) -> None:
        name = "Merry Xmas"
        if len(self.packages) > self.package_index:
            name = self.packages[self.package_index]

        name = list(name)
        name[0] = name[0].capitalize()

        self.state.package = "".join(name)

    def stop(self):
        if self.running:
            self.__information(
                "Application has been terminated, press Q to restore terminal."
            )

        self.running = False

    def run(self):
        self.__initialize_screen()
        self.running = True

        options = {
            'a': self.__add_packages,
            'r': self.__remove_packages,
            'n': self.__next_package,
            'p': self.__previous_package,
            's': lambda: 5
        }

        while self.running:
            try:
                option = self.__get_option()

                if option in options:
                    options[option]()
                elif option == 'q':
                    self.running = False
                else:
                    self.__information("{} is not an option".format(option))
            except Exception:
                self.__information("Press q to exit   ")

        self.__clean_screen()
