from abc import ABC, abstractmethod

class LoaderBase(ABC):
    @abstractmethod
    def load(self):
        pass
