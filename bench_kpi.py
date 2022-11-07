from os import listdir
from os.path import isfile, join
from macpacking.reader import DatasetReader, BinppReader
from macpacking.model import Online, Offline
from macpacking.algorithms.offline import FirstFitDecreasing, \
    BestFitDecreasing, WorstFitDecreasing, \
    MostTerribleDecreasing, GreedyHeuristic, RefinedFirstFitDecreasing
from macpacking.algorithms.offline import NextFit as NextFitOffline
import matplotlib
import matplotlib.pyplot as plt
import platform
from typing import Iterator


if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')
else:
    matplotlib.use('TkAgg')


# Entire binpp dataset is used to benchmark
# algorithms for KPIs: operations, comparisons.
ALL_CASES = []
base = './_datasets/binpp/N'
for i in range(1, 5):
    for j in range(1, 4):
        for k in [1, 2, 4]:
            ALL_CASES.append(base + str(i) +
                             'C' + str(j) + 'W' + str(k))
avg_optimal = 259

# type aliases
WeightStream = (int, Iterator[int])
Solution = list[list[int]]
KPI = str
Result = dict
Case = str


def main():
    '''this function calls all other benchmarking functions'''
    all_cases = []
    kpi = 'operations'
    for CASE in ALL_CASES:
        all_cases.append(list_case_files(CASE))

    # separate algorithms based on desired graphs
    quadratic_big = [NextFitOffline(), WorstFitDecreasing(),
                     RefinedFirstFitDecreasing()]
    quadratic_small = [FirstFitDecreasing(), BestFitDecreasing()]
    linear_c = [MostTerribleDecreasing(), GreedyHeuristic(avg_optimal)]
    offline_binpacker = quadratic_big + quadratic_small + linear_c

    plot_lines(offline_binpacker, all_cases, False, kpi, "all offline")


def list_case_files(dir: str) -> list[Case]:
    '''this function sorts and lists the case filenames'''
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


# measures kpi for many cases using a bin packing algorithm
# returns the average measurement for cases by number of weights
def run_bench_kpi(algorithm, cases: list[Case],
                  is_online: bool, kpi: KPI) -> Result:
    '''this function finds the average kpi measurement
    for an algorithm on many cases'''
    result = {}
    measurement = []
    # run algorithm on each case
    for case in cases:
        run = run_algorithm(algorithm, case, is_online)
        output = run['output']
        result['name'] = output['name']
        result['n'] = run['n']
        measurement.append(output[kpi])
    # take average kpi measurement for each n
    result['avg'] = sum(measurement) / len(measurement)
    return result


def plot_lines(algorithms: list, all_cases: list[list[Case]],
               is_online: bool, kpi: KPI, classify: str) -> None:
    '''this function plots a line graph of the kpi measurements
     for all algorithms on all cases'''
    data = {}
    last = 0
    point = {}
    # run algorithm on all cases
    for algo in algorithms:
        counter = 1
        first = True
        for cases in all_cases:
            result = run_bench_kpi(algo, cases, is_online, kpi)
            name = result['name']
            n = result['n']
            # separate points by n,
            # each point stores the average value for each n
            if first:
                point = (n, result['avg'])
                first = False
            elif last == n:
                new = point[1] + result['avg']
                point = (n, new)
                counter += 1
            else:
                new = point[1] / counter
                point = (last, new)
                if name not in data.keys():
                    data[name] = [point]
                else:
                    data[name].append(point)
                point = (n, result['avg'])
                counter = 1
            last = n
    # plot the values for each algorithm
    for algo in data.keys():
        points = data[algo]
        x = []
        y = []
        for p in points:
            x.append(p[0])
            y.append(p[1])
        plt.plot(x, y, label=algo)
        # print(algo)
        # print(y)
    plt.xlabel("Number of weights (n)")
    plt.ylabel(f"Number of {kpi}")
    plt.title(f"Measurement of {kpi} using {classify} \
        bin packing algorithms on binpp dataset")
    plt.legend()
    plt.show()


# runs bin packing algorithm on the given case
def run_algorithm(algorithm, case: str, is_online: bool) -> Result:
    '''this function runs the algorithm on a case and returns
    the result and number of items'''
    result = {}
    reader: DatasetReader
    reader = BinppReader(case)
    if is_online:
        strategy: Online = algorithm
        result['output'] = strategy(reader.online())
    else:
        strategy: Offline = algorithm
        result['output'] = strategy(reader.offline())
    result['n'] = 0
    # find n using the solution
    for soln in result['output']['solution']:
        result['n'] += len(soln)
    return result


if __name__ == "__main__":
    main()
