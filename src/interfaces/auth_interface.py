from abc import ABC, abstractmethod

class AuthInterface(ABC):
    @abstractmethod
    def login(self, username, password):
        pass

    @abstractmethod
    def register(self, username, password):
        pass
