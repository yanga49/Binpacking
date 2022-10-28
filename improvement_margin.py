import matplotlib
import matplotlib.pyplot as plt
import platform
from typing import List
from macpacking.reader import DatasetReader, BinppReader, JburkardtReader
from macpacking.model import Online, Offline
from macpacking.algorithms.online import NextFit, MostTerrible  # , FirstFit, BestFit, WorstFit
from macpacking.algorithms.offline import NextFit  # , FirstFitDecreasing, BestFitDecreasing, WorstFitDecreasing


if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')
else:
    matplotlib.use('TkAgg')

# REMEMBER TO TYPE ALIAS OUTPUT


class Margin:
    def __init__(self, optimal_filename, algorithm, is_online: bool):
        self.filepath = optimal_filename
        self.algorithm = algorithm
        self.is_online = is_online
        self.optimal = {}
        self.solutions = {}
        self.read_csv()
        self.run_algorithm()

    # this method defines the optimal_solutions solutions in a csv file as a dictionary
    def read_csv(self):
        csv_file = open(self.filepath, 'r')
        rows = []
        lines = csv_file.readlines()
        for line in lines:
            rows.append(line.split(","))
        for row in rows:
            self.optimal[row[0]] = row[1]

    # this method runs the algorithm for the specified dataset and returns the solution
    def run_algorithm(self):
        directory = ''
        length = 0
        reader: DatasetReader
        # determine directory name using filepath
        if self.filepath == 'optimal_solutions/binpp.csv':
            directory = 'binpp'
            length = 6
        elif self.filepath == 'optimal_solutions/binpphard.csv':
            directory = 'binpphard'
        elif self.filepath == 'optimal_solutions/jburkardt.csv':
            directory = 'jburkardt'

        for key in self.optimal.keys():
            if directory == 'binpp':
                dataset = f'datasets/{directory}/{key[0:length]}/{key}.BPP.txt'
                reader = BinppReader(dataset)
            elif directory == 'binpphard':
                dataset = f'datasets/{directory}/{key}.BPP.txt'
                reader = BinppReader(dataset)
            else:  # check if directory == 'jburkardt' if more DatasetReaders added
                datasetw = f'datasets/{directory}/{key}_w.BPP.txt'
                datasetc = f'datasets/{directory}/{key}_c.BPP.txt'
                reader = JburkardtReader(datasetw, datasetc)

            if self.is_online:
                strategy: Online = self.algorithm
                result = strategy(reader.online())
            else:
                strategy: Offline = self.algorithm
                result = strategy(reader.offline())
            self.solutions[key] = len(result)  # store number of bins in solutions[key]

    # this method returns whether the solutions are optimal_solutions or not
    def discrete_margin(self):
        pass

    # this method plots a bar graph of how many more bins the solutions use than the optimal_solutions solution does
    def continuous_margin(self):
        pass
