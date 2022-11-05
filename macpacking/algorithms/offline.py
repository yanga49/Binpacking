from .. import Solution, WeightSet
from ..model import Offline
from .online import NextFit as Nf_online
from .online import FirstFit as Ff_online
from .online import WorstFit as Wf_online
from .online import BestFit as Bf_online


class NextFit(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of NextFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Nf_online()
        return delegation((capacity, weights))


class FirstFitDecreasing(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of FirstFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Ff_online()
        return delegation((capacity, weights))
        

class BestFitDecreasing(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of BestFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Bf_online()
        return delegation((capacity, weights))

class WorstFitDecreasing(Offline):

    def _process(self, capacity: int, weights: WeightSet) -> Solution:
        '''An offline version of WorstFit, ordering the weigh stream and
        delegating to the online version (avoiding code duplication)'''
        weights = sorted(weights, reverse=True)
        delegation = Wf_online()
        return delegation((capacity, weights))


class GreedyHeuristic(Offline):

    def __init__(self, num_bins) -> None:
        super().__init__()
        self.num_bins = num_bins

    def _process(self, capacity: int, weights: list[int]) -> Solution:
        sums = [0] * self.num_bins
        partition = [[] for _ in range(self.num_bins)]
        for number in weights:
            smallest = min(range(len(sums)), key=sums.__getitem__)
            sums[smallest] += number
            partition[smallest].append(number)
        return partition
    
