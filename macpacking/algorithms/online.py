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
        res = 0
        # Create an array to store remaining space in bins
        # there can be at most n bins
        bin_rem = []
        solution = []
        
        # Place items one by one
        for w in stream:
            bin_rem.append([0])
        
            # Find the first bin that can accommodate
            # w
            j = 0
            while( j < res):
                if (bin_rem[j] >= w):
                    bin_rem[j] = bin_rem[j] - w
                    solution[j].append(w)
                    break
                j+=1
                
            # If no bin could accommodate w
            if (j == res):
                bin_rem[res] = capacity - w
                res = res+1
                solution.append([w])
        return solution


class BestFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        res = 0
    
        bin_rem = []
        solution = []
    
        for w in stream:
            bin_rem.append([0])
            j = 0
            min = capacity + 1
            bi = 0
    
            for j in range(res):
                if (bin_rem[j] >= w and bin_rem[j] - w < min):
                    bi = j
                    min = bin_rem[j] - w
                
            # If no bin could accommodate w,
            # create a new bin
            if (min == capacity + 1):
                bin_rem[res] = capacity - w
                res += 1
                solution.append([w])
            else: # Assign the item to best bin
                bin_rem[bi] -= w
                solution[j].append(w)
        return solution

class WorstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:
        # Initialize result (Count of bins)
        res = 0
    
        # Create an array to store remaining space in bins
        # there can be at most n bins
        bin_rem = []
        solution = []
        # Place items one by one
        for w in stream:
            bin_rem.append([0])
            # Find the best bin that ca\n accommodate
            # w
    
            # Initialize maximum space left and index
            # of worst bin
            mx,wi = -1,0
    
            for j in range(res):
                if (bin_rem[j] >= w and bin_rem[j] - w > mx):
                    wi = j
                    mx = bin_rem[j] - w
                
    
            # If no bin could accommodate w,
            # create a new bin
            if (mx == -1):
                bin_rem[res] = capacity - w
                res += 1
                solution.append([w])
            
            else: # Assign the item to best bin
                bin_rem[wi] -= w
                solution[j].append(w)
                
        
        return solution


