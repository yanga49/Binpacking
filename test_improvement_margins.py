from improvement_margin import Margin
from macpacking.algorithms.online import NextFit

test_jburk = Margin('optimal_solutions/jburkardt.csv',
                    NextFit(), 'Next Fit', True)
# read csv file to find optimal solutions
test_jburk.read_csv()
# run algorithm to find solutions
test_jburk.run_algorithm()
# find continuous margin


def test_continous():
    continous = test_jburk.continuous_margin()
    assert continous == {'p01': 0, 'p02': 1, 'p03': 0, 'p04': 1}


def test_discrete():
    discrete = test_jburk.discrete_margin()
    assert discrete == {'p01': True, 'p02': False, 'p03': True, 'p04': False}
