from .. import Result, WeightStream
from ..model import Online


class NextFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Result:
        result = {}
        bin_index = 0
        solution = [[]]
        operations = 0
        comparisons = 0
        remaining = capacity
        for w in stream:
            comparisons += 1
            if remaining >= w:
                solution[bin_index].append(w)
                remaining = remaining - w
                operations += 1
            else:
                bin_index += 1
                solution.append([w])
                remaining = capacity - w
                operations += 1
        result['solution'] = solution
        result['operations'] = operations
        result['comparisons'] = comparisons
        result['name'] = 'next fit'
        return result


class FirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Result:
        result = {}
        bin_count = 0
        bin_cap = []
        solution = []
        operations = 0
        comparisons = 0
        for w in stream:
            bin_cap.append([0])
            j = 0
            comparisons += 1
            while j < bin_count:
                comparisons += 1
                if bin_cap[j] >= w:
                    bin_cap[j] = bin_cap[j] - w
                    solution[j].append(w)
                    operations += 1
                    break
                j += 1
            comparisons += 1
            if j == bin_count:
                bin_cap[bin_count] = capacity - w
                bin_count = bin_count + 1
                solution.append([w])
                operations += 2
        result['solution'] = solution
        result['operations'] = operations
        result['comparisons'] = comparisons
        result['name'] = 'first fit'
        return result


class BestFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Result:
        result = {}
        bin_count = 0
        bin_cap = []
        solution = []
        operations = 0
        comparisons = 0
        for w in stream:
            bin_cap.append([0])
            j = 0
            min = capacity + 1
            bi = 0
            operations += 1
            for j in range(bin_count):
                comparisons += 2
                if bin_cap[j] >= w and bin_cap[j] - w < min:
                    bi = j
                    min = bin_cap[j] - w
                    operations += 1
            comparisons += 1
            if min == capacity + 1:
                bin_cap[bin_count] = capacity - w
                bin_count += 1
                solution.append([w])
                operations += 2
            else:
                bin_cap[bi] -= w
                solution[j].append(w)
                operations += 1
        result['solution'] = solution
        result['operations'] = operations
        result['comparisons'] = comparisons
        result['name'] = 'best fit'
        return result


class WorstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Result:
        result = {}
        bin_count = 0
        bin_cap = []
        solution = []
        operations = 0
        comparisons = 0
        j = 0
        for w in stream:
            bin_cap.append([0])
            mx, wi = -1, 0
            for j in range(bin_count):
                comparisons += 2
                if bin_cap[j] >= w and bin_cap[j] - w > mx:
                    wi = j
                    mx = bin_cap[j] - w
                    operations += 1
            comparisons += 1
            if mx == -1:
                bin_cap[bin_count] = capacity - w
                bin_count += 1
                solution.append([w])
                operations += 2
            else:
                bin_cap[wi] -= w
                solution[j].append(w)
                operations += 1
        result['solution'] = solution
        result['operations'] = operations
        result['comparisons'] = comparisons
        result['name'] = 'worst fit'
        return result


class MostTerrible(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Result:
        result = {}
        solution = [[]]
        operations = 0
        comparisons = 0
        for w in stream:
            comparisons += 1
            if w <= capacity:
                solution.append([w])
        result['solution'] = solution
        result['operations'] = operations
        result['comparisons'] = comparisons
        result['name'] = 'most terrible'
        return result

