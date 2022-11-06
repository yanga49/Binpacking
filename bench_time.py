import pyperf
from pyperf import BenchmarkSuite
from os import listdir
from os.path import isfile, join, basename, exists
from macpacking.reader import DatasetReader, BinppReader, JburkardtReader
from macpacking.model import Online, Offline
from macpacking.algorithms.baseline import BenMaier
from macpacking.algorithms.online import FirstFit, BestFit, WorstFit, MostTerrible
from macpacking.algorithms.online import NextFit as NextFitOnline
from macpacking.algorithms.offline import FirstFitDecreasing, BestFitDecreasing, WorstFitDecreasing
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
ALL_CASES = []
base = './_datasets/binpp/N'
for i in range(1, 5):
    for j in range(1, 4):
        for k in [1, 2, 4]:
            ALL_CASES.append(base + str(i) + 'C' + str(j) + 'W' + str(k))
WeightStream = (int, Iterator[int])
Solution = list[list[int]]
KPI = str
Result = dict
Case = str


def main():
    '''Example of benchmark code'''
    cases = list_case_files(CASES)
    online_binpacker = [NextFitOnline(), FirstFit(), BestFit(), WorstFit(), MostTerrible()]
    offline_binpacker = [NextFitOffline(), FirstFitDecreasing(), BestFitDecreasing(), WorstFitDecreasing()]
    # case = cases[0]
    # run_bench_time(online_binpacker, cases, True)
    # next_fit = load_bench_measurements('next fit', 'outputs/pyperf_measurements.json')
    # first_fit = load_bench_measurements('first fit', 'outputs/pyperf_measurements.json')
    # best_fit = load_bench_measurements('best fit', 'outputs/pyperf_measurements.json')
    # worst_fit = load_bench_measurements('worst fit', 'outputs/pyperf_measurements.json')
    # most_terrible = load_bench_measurements('most terrible', 'outputs/pyperf_measurements.json')
    vals = []
    for algo in ['next fit', 'first fit', 'best fit', 'worst fit', 'most terrible']:
        val = load_bench_measurements(algo, cases, 'outputs/pyperf_measurements.json')
        vals.append(val)
    plot_hist(vals)


def list_case_files(dir: str) -> list[str]:
    return sorted([f'{dir}/{f}' for f in listdir(dir) if isfile(join(dir, f))])


# def run_bench_time(case, algorithms: list, is_online) -> None:
#     """run the benchmark over a set of algorithm and the baseline"""
#     runner = pyperf.Runner()
#     if is_online:
#         data = BinppReader(case).online()
#     else:
#         data = BinppReader(case).offline()
#     runner.bench_func("python-binpacking", BenMaier(), data)
#     for algo in algorithms:
#         runner.bench_func(algo['name'], algo, data)

# def run_bench(cases: list[str]):
#     runner = pyperf.Runner()
#     for case in cases:
#         name = basename(case)
#         data = BinppReader(case).online()
#         binpacker = NextFit()
#         runner.bench_func(name, binpacker, data)


def run_bench_time(algorithms: list, cases: list, is_online):
    runner = pyperf.Runner()
    for algo in algorithms:
        for case in cases:
            name = run_algorithm(algo, case, is_online)['name'] + "_" + basename(case)
            if is_online:
                data = BinppReader(case).online()
            else:
                data = BinppReader(case).offline()
            runner.bench_func(name, algo, data)


def run_algorithm(algorithm, case: str, is_online):
    reader: DatasetReader
    reader = BinppReader(case)
    if is_online:
        strategy: Online = algorithm
        result = strategy(reader.online())
    else:
        strategy: Offline = algorithm
        result = strategy(reader.offline())
    return result


def load_bench_measurements(algo: str, cases: str, json_filename: str):
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
    canvas.hist(values, 5)


def plot_hist(vals: list):
    fig, axes = plt.subplots(1, len(vals), sharex=True, sharey=True)
    for val in range(len(vals)):
        draw_hist(vals[val][0], vals[val][1], axes[val])
    fig.tight_layout()
    plt.show()


# if __name__ == "__main__":
#     main()
main()
