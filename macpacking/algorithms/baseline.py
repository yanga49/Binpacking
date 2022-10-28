from .. import Solution
from ..model import Offline
import binpacking as bp


class BenMaier(Offline):

    def _process(self, capacity: int, weights: list[int]) -> Solution:
        return bp.to_constant_volume(weights, capacity)

class ConstantBinNumber(Offline):

    def __init__(self, num_bins) -> None:
        super().__init__()
        self.num_bins = num_bins

    def _process(self, capacity: int, weights: list[int]) -> Solution:
        return bp.to_constant_bin_number(weights, self.num_bins)