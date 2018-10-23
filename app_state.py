import logging
import colorlog
import os


class State():
    def __init__(self):
        self._package = "Ready for Xmas"
        self._logger, self._logfile = self.__setup_logging()

    def __setup_logging(self) -> "logger":
        logger = logging.getLogger("Client")
        if not os.path.isdir("./logging"):
            os.mkdir("./logging")

        logfile = open("./logging/log", "w")
        handler = colorlog.StreamHandler(logfile)
        formatter = colorlog.ColoredFormatter(
            fmt=('%(log_color)s[%(asctime)s %(levelname)8s] --'
                 ' %(message)s (%(filename)s:%(lineno)s)'),
            datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger, logfile

    @property
    def package(self) -> str:
        return self._package

    @package.setter
    def package(self, package: str) -> None:
        self._package = package

    @property
    def logger(self):
        return self._logger

    @property
    def logfile(self):
        return self._logfile

    def clean(self):
        self._logfile.flush()
        self._logfile.close()
