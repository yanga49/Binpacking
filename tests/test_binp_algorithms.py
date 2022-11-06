from macpacking.model  import Online, Offline
from macpacking.algorithms.online import NextFit, FirstFit, BestFit, WorstFit,RefinedFirstFit
from macpacking.algorithms.offline import NextFitDecreasing, FirstFitDecreasing, BestFitDecreasing, WorstFitDecreasing,RefinedFirstFitDecreasing
from macpacking.__init__ import WeightSet, WeightStream

# testing with a small number of weights
capacity = 10

def createWeightSet() -> WeightSet: # creating a weight set allowing for testing of offline algorithms
            unordered_weight_stream = [2,5,4,7,1,3,8]
            ordered_weight_set = sorted(unordered_weight_stream, reverse=True)
            return ordered_weight_set

def createWeightStream() -> WeightStream: # crating a weight stream allowing for the testing of online algorithms
            unordered_weight_stream = [2,5,4,7,1,3,8]
            return unordered_weight_stream

test_weightset = createWeightSet()
test_weightstream = createWeightStream()


def test_nextfit_online():
    strategy: Online = NextFit()
    result = strategy((capacity,test_weightstream))
    answer = [[8, 2], [7, 3], [5, 4, 1]]
    assert result['solution'] == answer


    
# testing the online algorithms 
def test_firstfit_online():
    strategy: Online = FirstFit()
    result = strategy((capacity,test_weightstream))
    answer = [[2, 5, 1], [4, 3], [7], [8]]
    assert result['solution'] == answer


def test_bestfit_online():
    strategy: Online = BestFit()
    result = strategy((capacity,test_weightstream))
    answer = [[2, 5, 1], [4], [7, 3], [8]]
    assert result['solution'] == answer


def test_worstfit_online():
    strategy: Online = WorstFit()
    result = strategy((capacity,test_weightstream))
    answer = [[2, 5], [4, 1, 3], [7], [8]]
    assert result['solution'] == answer


def test_refinedfirstfit_online():
    strategy: Online = RefinedFirstFit()
    result = strategy((capacity,test_weightstream))
    answer = [[7], [8], [4], [5], [2, 1, 3]]
    assert result['solution'] == answer


# testing offline algorithms
def test_nextfit_offline():
    strategy: Offline = NextFitDecreasing()
    result = strategy((capacity,test_weightset))
    answer = [[8], [7], [5, 4], [3, 2, 1]]
    assert result['solution'] == answer


def test_firstfit_offline():
    strategy: Offline = FirstFitDecreasing()
    result = strategy((capacity,test_weightset))
    answer = [[8, 2], [7, 3], [5, 4, 1]]
    assert result['solution'] == answer


def test_bestfit_offline():
    strategy: Offline = BestFitDecreasing()
    result = strategy((capacity,test_weightset))
    answer = [[8, 2], [7, 3], [5, 4, 1]]
    assert result['solution'] == answer

def test_worstfit_offline():
    strategy: Offline = WorstFitDecreasing()
    result = strategy((capacity,test_weightset))
    answer = [[8, 2], [7, 3], [5, 4, 1]]
    assert result['solution'] == answer


def test_refinedfirstfit_offline(): 
    strategy: Online = RefinedFirstFitDecreasing()
    result = strategy((capacity,test_weightset))
    answer = [[8], [7], [4], [5], [3, 2, 1]]
    assert result['solution'] == answer



