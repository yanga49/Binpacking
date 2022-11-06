from improvement_margin import Margin
from macpacking.algorithms.online import NextFit, MostTerrible
from macpacking.algorithms.offline import NextFit


test_binpp = Margin('optimal_solutions/jburkardt.csv', NextFit(), 'Next Fit', True, 'N1C1W1')
test_binpp.display_continuous()
print(test_binpp.optimal)
print(test_binpp.solutions)



