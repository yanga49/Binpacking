from improvement_margin import Margin
from macpacking.algorithms.online import NextFit, MostTerrible, FirstFit, BestFit, WorstFit
from macpacking.algorithms.offline import NextFit


test_binpp = Margin('optimal_solutions/jburkardt.csv', BestFit(), 'Best Fit Decreasing', False)
test_binpp.display_discrete()
test_binpp.display_continuous()
print(test_binpp.optimal)
print(test_binpp.solutions)
