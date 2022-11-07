from .. import Result, WeightStream
from ..model import Online
from .BinClass import BinClass
from .Piece import Piece


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
        # initalizing variables that will be useful when doing KPI comparisons
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
        # initalizing variables that will be useful when doing KPI comparisons
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
        solution = []
        # initalizing variables that will be useful when doing KPI comparisons
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

    def __init__(self) -> None:
        super().__init__()
        # initalizing variables that will be useful when doing KPI comparisons
        self.operations = 0
        self.comparisons = 0

    def _process(self, capacity: int, stream: WeightStream) -> Result:

        result = {}
        solution = [[]]
        b2Count = 0
        # list of all the bins of each class
        c1_bins = []
        c2_bins = []
        c3_bins = []
        c4_bins = []

        maxP = capacity  # used for normalization

        for w in stream:

            category = self.sort_pieces(w, maxP)
            w_piece = Piece(w, category)

            # if x-piece, add to a class 4 bin
            if w_piece.category == "small":
                self.comparisons += 1
                c4_bins = self.add_to_bin(capacity, "C4", c4_bins, w_piece)

            # if b2-piece, add to either class 1 or class 3 bin
            elif w_piece.category == "medium2":
                self.comparisons += 2
                b2Count += 1
                self.operations += 1
                self.comparisons += 4
                if (b2Count % 6 == 0) or (b2Count % 7 == 0) or \
                   (b2Count % 8 == 0) or (b2Count % 9 == 0):
                    c1_bins = self.add_to_bin(capacity, "C1", c1_bins, w_piece)
                else:
                    c3_bins = self.add_to_bin(capacity, "C3", c3_bins, w_piece)
            # if b1-piece, add to a class 2 bin
            elif w_piece.category == "medium1":
                self.comparisons += 3
                c2_bins = self.add_to_bin(capacity, "C2", c2_bins, w_piece)

            # if a-piece, add to a class 1 bin
            elif w_piece.category == "large":
                self.comparisons += 4
                c1_bins = self.add_to_bin(capacity, "C1", c1_bins, w_piece)

            else:
                self.comparisons += 4
        solution = self.get_pieces(c1_bins, solution) + \
            self.get_pieces(c2_bins, solution) + \
            self.get_pieces(c3_bins, solution) + \
            self.get_pieces(c4_bins, solution)
        self.operations += 1
        # important KPI evaluation metrics initalized
        result['solution'] = solution
        result['operations'] = self.operations
        result['comparisons'] = self.comparisons
        result['name'] = 'refined first fit'
        return result

    # function for extracting weights and bins from the class arrays
    def get_pieces(self, class_bins, solution) -> list[list[Piece]]:

        solution = [[]]

        for i in range(len(class_bins)):
            solution.append([])
            for j in range(len(class_bins[i].pieces)):
                piece = class_bins[i].pieces[j].weight
                solution[i].append(piece)

        return solution[:-1]

    # function responsible for adding
    # the piece to a bin, depending on it's class
    def add_to_bin(self, capacity, classID, class_bins, piece) -> list[Piece]:
        self.comparisons += 1
        # if there are no bins made in this class yet
        if len(class_bins) == 0:

            createBin = BinClass(capacity, classID)
            createBin.add_piece(piece)
            class_bins.append(createBin)

        else:

            for i in range(len(class_bins)):
                needBin = False
                self.comparisons += 1
                if class_bins[i].remaining >= piece.weight:
                    self.comparisons += 2
                    if piece.category == "medium2" and classID == "C1":
                        self.comparisons += 1
                        if self.check_bin(class_bins[i]):
                            class_bins[i].add_piece(piece)
                            break

                    # this is for every other category, besides B2
                    class_bins[i].add_piece(piece)
                    break
                needBin = True

            # make new bin for piece
            if needBin:
                createBin = BinClass(capacity, classID)
                createBin.add_piece(piece)
                class_bins.append(createBin)

        return class_bins

    # function to check if the bin has an A-piece,
    # as it is a requirement for a B2-piece to be added to the bin
    def check_bin(self, class_bin: BinClass):
        for i in class_bin.pieces:
            self.comparisons += 1
            if i.category == "large":
                return True

    # sorts weight into its piece category
    def sort_pieces(self, w: int, max: int) -> str:

        # normalize the interval
        x_max = max * 1 / 3
        b2_max = max * 2 / 5
        b1_max = max * 1 / 2
        self.operations += 3

        # X-piece
        if w <= x_max:
            self.comparisons += 1
            return "small"

        # B2-piece
        elif x_max < w <= b2_max:
            self.comparisons += 2
            return "medium1"

        # B1-piece
        elif b2_max < w <= b1_max:
            self.comparisons += 3
            return "medium2"

        # A-piece
        elif b1_max < w <= max:
            self.comparisons += 4
            return "large"

        else:
            self.comparisons += 4
