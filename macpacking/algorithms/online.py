from .. import Result,Solution, WeightStream
from ..model import Online
from binClasses import binClasses
from Piece import Piece


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
                solution[bi].append(w)
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
            # if no bin can accomodate weight, new bin has to be created
            if mx == -1:
                bin_cap[bin_count] = capacity - w
                bin_count += 1
                solution.append([w])
                operations += 2
            else:
                bin_cap[wi] -= w
                solution[wi].append(w)
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

class RefinedFirstFit(Online):

    def _process(self, capacity: int, stream: WeightStream) -> Solution:

        solution = [[]]
        b2Count = 0

        c1_bins = []
        c2_bins = []
        c3_bins = []
        c4_bins = []

        maxP = capacity

        for w in stream:

            category = self.sortPieces(w, maxP)
            w_piece = Piece(w, category)

            #if x-piece, add to a class 4 bin
            if w_piece.category == "small":
                c4_bins = self.add_to_bin(capacity, "C4", c4_bins, w_piece)

            elif w_piece.category == "medium2":
                b2Count += 1

                if (b2Count % 6 == 0) or (b2Count % 7 == 0) or (b2Count % 8 == 0) or (b2Count % 9 == 0):
                    c1_bins = self.add_to_bin(capacity, "C1", c1_bins, w_piece)

                else:
                    c3_bins = self.add_to_bin(capacity, "C3", c3_bins, w_piece)\

            elif w_piece.category == "medium1":
                c2_bins = self.add_to_bin(capacity, "C2", c2_bins, w_piece)
                

            elif w_piece.category == "large":
                c1_bins = self.add_to_bin(capacity, "C1", c1_bins, w_piece)

        solution = self.get_pieces(c1_bins, solution) + self.get_pieces(c2_bins, solution) + self.get_pieces(c3_bins, solution) + self.get_pieces(c4_bins, solution)

        return solution
        

    def get_pieces(self, class_bins, solution):

        solution = [[]]

        for i in range(len(class_bins)):
            solution.append([])
            for j in range(len(class_bins[i].pieces)):
                piece = class_bins[i].pieces[j].weight
                solution[i].append(piece)

        return solution[:-1]

        
    def add_to_bin(self, capacity, classID, class_bins, piece):

        if len(class_bins) == 0:   
            createBin = binClasses(capacity, classID)
            createBin.add_piece(piece)
            class_bins.append(createBin)

        else:

            for i in range(len(class_bins)):
                needBin = False
                if class_bins[i].remaining >= piece.weight:

                    if piece.category == "medium2" and classID == "C1":
                        if self.check_bin(class_bins[i]):
                            class_bins[i].add_piece(piece)
                            break
                    
                    class_bins[i].add_piece(piece)
                    break
                needBin = True

            if needBin:
                createBin = binClasses(capacity, classID)
                createBin.add_piece(piece)
                class_bins.append(createBin)
        
        return class_bins

    def check_bin(self, class_bin : binClasses):
        for i in class_bin.pieces:
            if i.category == "large":
                return True

    def sortPieces(self, w : int, max : int) -> str:

        x_max = max * 1/3
        b2_max = max * 2/5
        b1_max = max * 1/2


        # X-piece
        if w <= x_max:
            return "small"

        #B2-piece
        elif x_max < w <= b2_max:
            return "medium1"
            
        #B1-piece
        elif b2_max < w <= b1_max:
            return "medium2"

        #A-piece
        elif b1_max < w <= max:
            return "large"
