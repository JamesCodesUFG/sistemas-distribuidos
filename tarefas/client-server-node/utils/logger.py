from enum import Enum

from threading import Lock

class LogType(Enum):
    LOG = 0
    ERROR = 1
    WARNING = 2

class Logger:
    __logs: list['Log'] = []

    __lock: Lock = Lock()

    def log(self, message: str, tags: list[str] = []):
        self.__lock.acquire()
        self.__logs.append(Log(message, LogType.LOG, tags))
        self.__lock.release()

    def error(self, message: str, tags: list[str] = []):
        self.__lock.acquire()
        self.__logs.append(Log(message, LogType.ERROR, tags))
        self.__lock.release()

    def warning(self, message: str, tags: list[str] = []):
        self.__lock.acquire()
        self.__logs.append(Log(message, LogType.WARNING, tags))
        self.__lock.release()

    def print(self):
        for log in self.__logs:
            log.print()

class Log:
    def __init__(self, message: str, type: LogType, tags: list[str]=[]):
        self.message = message
        self.type = type
        self.tags = tags

    def print(self):
        match self.type:
            case LogType.LOG:
                print("\033[34m[LOG]\033[0m", self.message)
            case LogType.ERROR:
                print("\033[31m[ERR]\033[0m", self.message)
            case LogType.WARNING:
                print("\033[33m[WRN]\033[0m", self.message)

    # TODO: Implementar um filtro de tags ou por tipo.
    def filter(self) -> bool:
        pass