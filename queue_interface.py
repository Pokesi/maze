from abc import ABC, abstractmethod


class Queue(ABC):
    @abstractmethod
    def put(self, value): ...

    @abstractmethod
    def get(self): ...

    @abstractmethod
    def empty(self): ...

    @abstractmethod
    def size(self): ...
