import time
import curses
from app_gui import Gui
from curses.textpad import Textbox
from overrides import overrides


class GuiImpl(Gui):
    def __init__(self, *args):
        Gui.__init__(self, *args)

        self.packages = []
        self.package_index = 0
        """ Window Objects. """
        self.display_window = None
        self.input_window = None
        self.textbox_win = None
        self.stdscr = None

        self.running = False

    def __display_packages(self) -> None:
        X_index = 1
        for index, package in enumerate(
                reversed(self.packages[:self.package_index])):

            Y_index = (index % (curses.LINES - 2)) + 1

            if X_index > curses.COLS:
                break

            self.display_window.addstr(Y_index, X_index, "{} - {}".format(
                index, package), curses.A_BOLD)

            if (index + 1) % (curses.LINES - 2) == 0:
                X_index += 15

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

        self.__refresh_display_page()
        self.__refresh_input_page()

    def __clean_screen(self) -> None:
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def __refresh_input_page(self, indicator="") -> None:
        self.input_window.clear()
        self.input_window.border()
        self.input_window.addstr(
            int(curses.LINES / 30), int(curses.COLS / 30),
            "Add [a] - Remove [r] - Next [n] - Previous Package [p] - Sort [s]",
            curses.A_UNDERLINE)

        self.input_window.addstr(4 * int(curses.LINES / 30),
                                 1 * int(curses.COLS / 30), "Mode: ",
                                 curses.A_BOLD)

        self.input_window.addstr(4 * int(curses.LINES / 30),
                                 2 * int(curses.COLS / 30), indicator,
                                 curses.A_STANDOUT)
        self.input_window.refresh()

    def __refresh_display_page(self) -> None:
        self.display_window.clear()
        self.display_window.border()
        self.display_window.refresh()

    def __information(self, text: str) -> None:
        self.input_window.addstr(3 * int(curses.LINES / 30),
                                 1 * int(curses.COLS / 30),
                                 "Information: {}".format(text), curses.A_BOLD)
        self.input_window.refresh()

    def __textbox_input(self) -> str:
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

        self.__refresh_input_page()

        return message

    def __add_packages(self) -> None:
        self.__refresh_input_page("a")
        self.__information("Input the name of packages to add")
        """ Parse the inputs. """
        for package in self.__textbox_input().split("\n"):
            package = package.strip().lower()

            if len(package) > 0:
                self.packages.append(package)

        self.package_index = len(self.packages)
        self.__display_packages()
        self.__information("Add successful")

    def __remove_packages(self) -> None:
        self.__refresh_input_page("r")
        self.__information("Input the index of packages to remove")
        """ Parse the numbers """
        for package_index in self.__textbox_input().split("\n"):
            index = None
            try:
                index = int(package_index.strip())
            except ValueError:
                continue

            absolute_index = self.package_index - index - 1

            if absolute_index >= 0 and absolute_index < len(self.packages):
                del self.packages[absolute_index]
        """ Remove removed packages from list. """
        packages = []
        for package in self.packages:
            if package is not None:
                packages.append(package)
        """ Update packages & Index. """
        self.packages = packages
        self.package_index = min(self.package_index, len(self.packages))

        self.__refresh_display_page()
        self.__display_packages()
        self.__information("Removed successful")

    def __next_package(self) -> None:
        self.__refresh_display_page()
        self.__refresh_input_page("n")
        self.package_index -= 1

        if self.package_index < 0:
            self.package_index = 0

        self.__display_packages()
        self.__update_server_package()

    def __previous_package(self) -> None:
        self.__refresh_display_page()
        self.__refresh_input_page("p")
        self.package_index += 1

        if self.package_index > len(self.packages):
            self.package_index = len(self.packages)

        self.__display_packages()
        self.__update_server_package()

    def __get_option(self) -> str:
        return chr(
            self.input_window.getch(10 * int(curses.LINES / 30),
                                    9 * int(curses.COLS / 30)))

    def __update_server_package(self) -> None:
        name = "Merry Xmas"
        if len(self.packages) > self.package_index >= 0:
            name = self.packages[self.package_index]
        """ Format the name in a nice way. Captialize is nice!"""
        name = list(name)
        name[0] = name[0].capitalize()

        self.state.package = "".join(name)

    def __sort_packages(self) -> None:
        self.__refresh_display_page()
        self.__refresh_input_page("s")
        """ Sorts the packages. """
        self.packages = self.santa(self.packages)
        """ Update Screen. """
        self.__display_packages()
        """ Get them stats. """
        heuristic_score, goal_score, random_score, order_score = self.santa.sorting_statistics(
            self.packages)
        """ Display score. """
        self.__information(
            "Heuristic: {} - Goal {} - Random {} - Order {}".format(
                round(heuristic_score, 3), round(goal_score, 3),
                round(random_score, 3), round(order_score, 3)))

    @overrides
    def stop(self) -> None:
        if self.running:
            self.__information(
                "Application has been terminated, press Q to restore terminal."
            )

        self.running = False

    @overrides
    def run(self):
        self.__initialize_screen()
        self.running = True

        options = {
            'a': self.__add_packages,
            'r': self.__remove_packages,
            'n': self.__next_package,
            'p': self.__previous_package,
            's': self.__sort_packages
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
            except Exception as e:
                self.__information("Press q to exit: {}   ".format(e))

        self.__clean_screen()
