from macpacking.model import Online, Offline
from macpacking.algorithms.online import NextFit, FirstFit, BestFit, \
    WorstFit, RefinedFirstFit
from macpacking.algorithms.offline import NextFitDecreasing, \
    FirstFitDecreasing, BestFitDecreasing, WorstFitDecreasing, \
    RefinedFirstFitDecreasing
from macpacking.__init__ import WeightSet, WeightStream

# testing each algorithm with an extremely large number of weights
capacity = 100


# creating a weight set allowing for testing of offline algorithms
def createWeightSet() -> WeightSet:
    unordered_weight_stream = [21, 30, 52, 85, 99, 14, 17, 20, 3, 22, 23,
                               24, 25, 27, 28, 28, 29, 30, 7, 33, 33, 40,
                               40, 42, 44, 46, 49, 51, 7, 56, 61, 62, 67,
                               67, 69, 72, 74, 76, 10, 86, 87, 88, 91, 92,
                               92, 96, 96, 99, 11, 13]
    ordered_weight_set = sorted(unordered_weight_stream, reverse=True)
    return ordered_weight_set


# crating a weight stream allowing for the testing of online algorithms
def createWeightStream() -> WeightStream:
    unordered_weight_stream = [21, 30, 52, 85, 99, 14, 17, 20, 3, 22, 23,
                               24, 25, 27, 28, 28, 29, 30, 7, 33, 33, 40,
                               40, 42, 44, 46, 49, 51, 7, 56, 61, 62, 67,
                               67, 69, 72, 74, 76, 10, 86, 87, 88, 91, 92,
                               92, 96, 96, 99, 11, 13]
    return unordered_weight_stream


test_weightset = createWeightSet()
test_weightstream = createWeightStream()


# testing the online algorithms
def test_nextfit_online2():
    strategy: Online = NextFit()
    result = strategy((capacity, test_weightstream))
    print(result['solution'])
    answer = [[21, 30], [52], [85], [99], [14, 17, 20, 3, 22, 23],
              [24, 25, 27], [28, 28, 29], [30, 7, 33], [33, 40], [40, 42],
              [44, 46], [49, 51], [7, 56], [61], [62], [67], [67], [69],
              [72], [74], [76, 10], [86], [87], [88], [91], [92], [92], [96],
              [96], [99], [11, 13]]
    assert result['solution'] == answer


def test_firstfit_online2():
    strategy: Online = FirstFit()
    result = strategy((capacity, test_weightstream))
    answer = [[21, 30, 14, 17, 3, 7, 7], [52, 20, 22], [85, 10],
              [99], [23, 24, 25, 27], [28, 28, 29, 11],
              [30, 33, 33], [40, 40, 13], [42, 44], [46, 49], [51],
              [56], [61], [62], [67], [67], [69], [72], [74], [76], [86],
              [87], [88], [91], [92], [92], [96], [96], [99]]
    assert result['solution'] == answer


def test_bestfit_online2():
    strategy: Online = BestFit()
    result = strategy((capacity, test_weightstream))
    answer = [[21, 30, 22, 23], [52, 17, 20, 3, 7], [85, 14], [99],
              [24, 25, 27], [28, 28, 29, 10], [30, 33, 33], [40, 40],
              [42, 44, 7], [46, 49], [51], [56], [61], [62], [67],
              [67], [69], [72], [74], [76], [86], [87, 13], [88, 11],
              [91], [92], [92], [96], [96], [99]]
    assert result['solution'] == answer


def test_worstfit_online2():
    strategy: Online = WorstFit()
    result = strategy((capacity, test_weightstream))
    answer = [[21, 30, 14, 20], [52, 17, 3, 22], [85], [99], [23, 24, 25, 27],
              [28, 28, 29], [30, 7, 33, 7], [33, 40], [40, 42], [44, 46],
              [49, 51], [56, 10], [61, 11], [62, 13], [67], [67], [69], [72],
              [74], [76], [86], [87], [88], [91], [92], [92], [96], [96],
              [99]]
    assert result['solution'] == answer


def test_refinedfirstfit_online2():
    strategy: Online = RefinedFirstFit()
    result = strategy((capacity, test_weightstream))
    answer = [[52], [85], [99], [51], [56], [61], [62], [67], [67], [69],
              [72], [74], [76], [86], [87], [88], [91], [92], [92], [96],
              [96], [99], [40, 40], [42, 44], [46, 49],
              [21, 30, 14, 17, 3, 7, 7], [20, 22, 23, 24, 10],
              [25, 27, 28, 11], [28, 29, 30, 13], [33, 33]]
    assert result['solution'] == answer


# testing offline algorithms
def test_nextfit_offline2():
    strategy: Offline = NextFitDecreasing()
    result = strategy((capacity, test_weightset))
    answer = [[99], [99], [96], [96], [92], [92], [91], [88], [87], [86],
              [85], [76], [74], [72], [69], [67], [67], [62], [61], [56],
              [52], [51, 49], [46, 44], [42, 40], [40, 33], [33, 30, 30],
              [29, 28, 28], [27, 25, 24, 23], [22, 21, 20, 17, 14],
              [13, 11, 10, 7, 7, 3]]
    assert result['solution'] == answer


def test_firstfit_offline2():
    strategy: Offline = FirstFitDecreasing()
    result = strategy((capacity, test_weightset))
    answer = [[99], [99], [96, 3], [96], [92, 7], [92, 7], [91],
              [88, 11], [87, 13], [86, 14], [85, 10], [76, 24],
              [74, 25], [72, 28], [69, 30], [67, 33], [67, 33],
              [62, 30], [61, 29], [56, 44], [52, 46], [51, 49],
              [42, 40, 17], [40, 28, 27], [23, 22, 21, 20]]
    assert result['solution'] == answer


def test_bestfit_offline2():
    strategy: Offline = BestFitDecreasing()
    result = strategy((capacity, test_weightset))
    answer = [[99], [99], [96, 3], [96], [92, 7], [92, 7], [91], [88, 11],
              [87, 13], [86, 14], [85], [76, 24], [74, 25], [72, 28],
              [69, 30], [67, 33], [67, 33], [62, 30], [61, 29, 10],
              [56, 44], [52, 46], [51, 49], [42, 40, 17], [40, 28, 27],
              [23, 22, 21, 20]]
    assert result['solution'] == answer


def test_worstfit_offline2():
    strategy: Offline = WorstFitDecreasing()
    result = strategy((capacity, test_weightset))
    answer = [[99], [99], [96], [96], [92, 3], [92], [91, 7], [88, 7],
              [87, 10], [86, 13], [85, 14], [76, 24], [74, 25], [72, 28],
              [69, 28], [67, 30], [67, 29], [62, 30], [61, 33], [56, 44],
              [52, 46], [51, 49], [42, 40, 17], [40, 33, 27],
              [23, 22, 21, 20, 11]]
    assert result['solution'] == answer


def test_refinedfirstfit_offline2():
    strategy: Online = RefinedFirstFitDecreasing()
    result = strategy((capacity, test_weightset))
    answer = [[99], [99], [96], [96], [92], [92], [91], [88],
              [87], [86], [85], [76], [74], [72], [69], [67], [67],
              [62], [61], [56], [52], [51], [40, 40], [49, 46],
              [44, 42], [33, 33, 30, 3], [30, 29, 28, 13],
              [28, 27, 25, 20], [24, 23, 22, 21, 10],
              [17, 14, 11, 7, 7]]
    assert result['solution'] == answer
