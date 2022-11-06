import pyperf
from pyperf import BenchmarkSuite
from os import listdir
from os.path import isfile, join, basename, exists
from macpacking.reader import DatasetReader, BinppReader, JburkardtReader
from macpacking.model import Online, Offline
from macpacking.algorithms.baseline import BenMaier
from macpacking.algorithms.online import FirstFit, BestFit, WorstFit, MostTerrible, RefinedFirstFit
from macpacking.algorithms.online import NextFit as NextFitOnline
from macpacking.algorithms.offline import FirstFitDecreasing, BestFitDecreasing, WorstFitDecreasing, \
    MostTerribleDecreasing, GreedyHeuristic, RefinedFirstFitDecreasing
from macpacking.algorithms.offline import NextFit as NextFitOffline
import matplotlib
import matplotlib.pyplot as plt
import platform
import argparse
import binpacking
from typing import Iterator


if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')
else:
    matplotlib.use('TkAgg')


# We consider:
#   - 500 objects (N4)
#   - bin capacity of 120 (C2)
#   - and weight in the [20,100] interval (W2)
CASES = './_datasets/binpp/N4C2W2'
optimal = 253

# type aliases
WeightStream = (int, Iterator[int])
Solution = list[list[int]]
KPI = str
Result = dict
Case = str


def main():
    cases = list_case_files(CASES)
    online_binpacker = [NextFitOnline(), FirstFit(), BestFit(), WorstFit(), MostTerrible(), RefinedFirstFit()]
    offline_binpacker = [NextFitOffline(), FirstFitDecreasing(), BestFitDecreasing(), MostTerribleDecreasing(),
                         WorstFitDecreasing(), GreedyHeuristic(optimal), RefinedFirstFitDecreasing()]
    vals = []
    case = [cases[0]]
    run_bench_time(offline_binpacker, case, False)
    # linear = ['greedy', 'most terrible', 'next fit']
    # nonlinear = ['first fit', 'best fit', 'worst fit', 'refined first fit', 'python-binpacking']
    # all_names = linear + nonlinear
    # for algo in all_names:
    #     val = load_bench_measurements(algo, case, 'outputs/pyperf_measurements_offline_case.json')
    #     vals.append(val)
    # plot_hist(vals)


def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


def run_bench_time(algorithms: list, cases: list, is_online) -> None:
    runner = pyperf.Runner()
    for algo in algorithms:
        for case in cases:
            name = run_algorithm(algo, case, is_online)['name'] + "_" + basename(case)
            if is_online:
                data = BinppReader(case).online()
            else:
                data = BinppReader(case).offline()
            runner.bench_func(name, algo, data)
    for case in cases:
        name = "python-binpacking_" + basename(case)
        if not is_online:
            data = BinppReader(case).offline()
            runner.bench_func(name, BenMaier(), data)


def run_algorithm(algorithm, case: str, is_online) -> Result:
    reader: DatasetReader
    reader = BinppReader(case)
    if is_online:
        strategy: Online = algorithm
        result = strategy(reader.online())
    else:
        strategy: Offline = algorithm
        result = strategy(reader.offline())
    return result


def load_bench_measurements(algo: str, cases: list[str], json_filename: str) -> (list, str):
    """extract the values for a given benchmark"""
    suite = BenchmarkSuite.load(json_filename)
    values = []
    for case in cases:
        name = algo + "_" + basename(case)
        bench = suite.get_benchmark(name)
        values += list(bench.get_values())
    return values, algo


def draw_hist(values: list[float], title: str, canvas):
    canvas.set_title(title)
    canvas.set(xlabel='exec time (s)', ylabel='|instances|')
    canvas.hist(values, 10)


def plot_hist(vals: list):
    # fig, axes = plt.subplots(1, len(vals), sharex=True, sharey=True)
    for val in range(len(vals)):
        plt.hist(vals[val][0], bins=10, label=vals[val][1])
        # draw_hist(vals[val][0], vals[val][1], axes[val])
    plt.title("Execution time for non-linear offline bin packing algorithms on binpp dataset N4C2W2_A")
    plt.xlabel("Execution time (s)")
    plt.ylabel("Instances")
    plt.legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    main()
