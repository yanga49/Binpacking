from abc import ABC, abstractmethod
from typing import Iterator
from . import WeightStream, WeightSet, Result


class BinPacker(ABC):
    pass


class Online(BinPacker):

    def __call__(self, ws: WeightStream):
        capacity, stream = ws
        return self._process(capacity, stream)

    @abstractmethod
    def _process(self, c: int, stream: Iterator[int]) -> Result:
        pass


class Offline(BinPacker):

    def __call__(self, ws: WeightSet):
        capacity, weights = ws
        return self._process(capacity, weights)

    @abstractmethod
    def _process(self, c: int, weights: list[int]) -> Result:
        pass
