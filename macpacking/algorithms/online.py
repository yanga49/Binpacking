from .. import Solution, WeightStream
from ..model import Online


class NextFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_index = 0
        solution = [[]]
        remaining = capacity
        for w in stream:
            if remaining >= w:
                solution[bin_index].append(w)
                remaining = remaining - w
            else:
                bin_index += 1
                solution.append([w])
                remaining = capacity - w
        return solution


class FirstFit(Online):
    
    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_count = 0
        bin_cap = []
        solution = []
        for w in stream:
            bin_cap.append([0])
            j = 0
            while (j < bin_count):
                if (bin_cap[j] >= w):
                    bin_cap[j] = bin_cap[j] - w
                    solution[j].append(w)
                    break
                j+=1
            if (j == bin_count):
                bin_cap[bin_count] = capacity - w
                bin_count = bin_count+1
                solution.append([w])
        return solution


class BestFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_count = 0
    
        bin_cap = []
        solution = []
    
        for w in stream:
            bin_cap.append([0])
            j = 0
            min = capacity + 1
            bi = 0
    
            for j in range(bin_count):
                if (bin_cap[j] >= w and bin_cap[j] - w < min):
                    bi = j
                    min = bin_cap[j] - w
                
            if (min == capacity + 1):
                bin_cap[bin_count] = capacity - w
                bin_count += 1
                solution.append([w])
            else: 
                bin_cap[bi] -= w
                solution[j].append(w)
        return solution

class WorstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        bin_count = 0
        bin_cap = []
        solution = []
        for w in stream:
            bin_cap.append([0])
            mx,wi = -1,0
    
            for j in range(bin_count):
                if (bin_cap[j] >= w and bin_cap[j] - w > mx):
                    wi = j
                    mx = bin_cap[j] - w
            
            if (mx == -1):
                bin_cap[bin_count] = capacity - w
                bin_count += 1
                solution.append([w])
            
            else:
                bin_cap[wi] -= w
                solution[j].append(w)
                
        return solution


