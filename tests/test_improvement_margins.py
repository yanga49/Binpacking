from ..improvement_margin import Margin
from ..macpacking.algorithms.online import NextFit, MostTerrible
from ..macpacking.algorithms.offline import NextFitDecreasing

test_binpp = Margin('optimal_solutions/jburkardt.csv', NextFit(), 'Next Fit', True)

def test_continous():
    test_binpp.display_continuous()
    assert test_binpp.optimal == {'p01': 4, 'p02': 7, 'p03': 4, 'p04': 7}
    assert test_binpp.solutions == {'p01': 4, 'p02': 8, 'p03': 4, 'p04': 8}

def test_discrete():
    discrete = test_binpp.discrete_margin()
    assert discrete == {'p01': True, 'p02': False, 'p03': True, 'p04': False}

