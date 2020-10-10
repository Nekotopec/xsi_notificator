from abc import ABC, abstractmethod
from typing import NamedTuple


class Loader(ABC):

    @abstractmethod
    def load(self, data: NamedTuple):
        """
        Load info about add to remote database.
        """
        pass


class ExcellLoader(Loader):

    def __init__(self):
        self.file =


    def load(self, data):
        pass
