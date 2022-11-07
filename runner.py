from improvement_margin import Margin
from macpacking.algorithms.online import NextFit


test_binpp = Margin('optimal_solutions/jburkardt.csv',
                    NextFit(), 'Next Fit', True)
test_binpp.display_continuous()
print(test_binpp.optimal)
print(test_binpp.solutions)
print(test_binpp.discrete_margin())
