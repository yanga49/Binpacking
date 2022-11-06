from improvement_margin import Margin
from macpacking.algorithms.online import NextFit, MostTerrible, WorstFit, BestFit, RefinedFirstFit
from macpacking.algorithms.offline import NextFitDecreasing, WorstFitDecreasing, BestFitDecreasing, RefinedFirstFitDecreasing


test_binpp = Margin('optimal_solutions/jburkardt.csv', NextFit(), 'Next Fit', True)
test_binpp.display_continuous()
print(test_binpp.optimal)
print(test_binpp.solutions)
print(test_binpp.discrete_margin())



