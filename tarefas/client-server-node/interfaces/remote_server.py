from abc import *

class RemoteServer(ABC):

    @abstractmethod
    def get(self, file_name):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def post(self, file_name, data):
        pass

    @abstractmethod
    def delete(self, file_name):
        pass