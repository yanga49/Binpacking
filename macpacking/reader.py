from abc import ABC, abstractmethod
from os import path
from random import shuffle, seed
from . import WeightSet, WeightStream


class DatasetReader(ABC):

    def offline(self) -> WeightSet:
        '''Return a WeightSet to support an offline algorithm'''
        (capacity, weights) = self._load_data_from_disk()
        seed(42)          # always produce the same shuffled result
        shuffle(weights)  # side effect shuffling
        return (capacity, weights)

    def online(self) -> WeightStream:
        '''Return a WeighStream, to support an online algorithm'''
        (capacity, weights) = self.offline()

        def iterator():  # Wrapping the contents into an iterator
            for w in weights:
                yield w  # yields the current value and moves to the next one

        return (capacity, iterator())

    @abstractmethod
    def _load_data_from_disk(self) -> WeightSet:
        '''Method that read the data from disk, depending on the file format'''
        pass


class BinppReader(DatasetReader):
    '''Read problem description according to the BinPP format'''

    def __init__(self, filename: str) -> None:
        if not path.exists(filename):
            raise ValueError(f'Unkown file [{filename}]')
        self.__filename = filename

    def _load_data_from_disk(self) -> WeightSet:
        with open(self.__filename, 'r') as reader:
            nb_objects: int = int(reader.readline())
            capacity: int = int(reader.readline())
            weights = []
            for _ in range(nb_objects):
                weights.append(int(reader.readline()))
            return (capacity, weights)

class JburkardtReader(DatasetReader):
    '''Read problem description according to the jburkardt format'''

    def __init__(self, pfilename: str, cfilename: str) -> None:
        if not path.exists(cfilename):
            raise ValueError(f'Unkown file [{cfilename}]')
        elif not path.exists(pfilename):
            raise ValueError(f'Unkown file [{pfilename}]')
        self.__cfilename = cfilename
        self.__pfilename = pfilename

    def _load_data_from_disk(self) -> WeightSet:
        with open(self.__cfilename, 'r') as reader:
            capacity: int = int(reader.readline()[:-1])

        with open(self.__pfilename, 'r') as reader2:
            lines = reader2.readlines()
            weights = []
            for line in lines:
                if line != "\n":
                    weights.append(int(line.strip()))
            
        return (capacity, weights)
