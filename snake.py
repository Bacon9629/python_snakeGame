from abc import ABC,abstractmethod

class Snake(ABC):
    @property
    @abstractmethod
    def step(self):
        pass

    @property
    @abstractmethod
    def width(self):
        pass

    @abstractmethod
    def create_body(self):
        pass

    @abstractmethod
    def add_body(self):
        pass

    @abstractmethod
    def move_body(self):
        pass