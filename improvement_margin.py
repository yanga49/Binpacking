import matplotlib
import matplotlib.pyplot as plt
import platform
from macpacking.reader import DatasetReader, BinppReader, JburkardtReader
from macpacking.model import Online, Offline


if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')
else:
    matplotlib.use('TkAgg')

# type aliases
Filename = str
Algorithm = str
Discrete = dict
Continuous = dict


class Margin:
    def __init__(self, optimal_filename: Filename, algorithm, algo_name: Algorithm, is_online: bool, case=' ') -> None:
        self.filepath = optimal_filename
        self.algorithm = algorithm
        self.algo_name = algo_name
        self.is_online = is_online
        self.optimal = {}
        self.solutions = {}
        self.directory = ''
        self.case = False
        if self.filepath == 'optimal_solutions/binpp.csv':
            if case == ' ':
                self.directory = 'binpp'
            else:
                self.directory = case
                self.case = True
        elif self.filepath == 'optimal_solutions/binpp-hard.csv':
            self.directory = 'binpp-hard'
        elif self.filepath == 'optimal_solutions/jburkardt.csv':
            self.directory = 'jburkardt'

    # this method defines the optimal_solutions solutions in a csv file as a dictionary
    def read_csv(self) -> None:
        # initialize empty dictionary
        self.optimal = {}
        csv_file = open(self.filepath, 'r')
        rows = []
        lines = csv_file.readlines()
        for line in lines:
            rows.append(line.split(","))
        rows.pop(0)
        for row in rows:
            self.optimal[row[0]] = int(row[1])

    # this method runs the algorithm for the specified dataset and returns the solution
    def run_algorithm(self) -> None:
        # initialize empty dictionary
        self.solutions = {}
        reader: DatasetReader
        for key in self.optimal.keys():
            if self.directory == 'binpp':
                dataset = f'_datasets/{self.directory}/{key[0:6]}/{key}.BPP.txt'
                reader = BinppReader(dataset)
            elif self.directory == 'binpp-hard':
                dataset = f'_datasets/{self.directory}/{key}.BPP.txt'
                reader = BinppReader(dataset)
            elif self.directory == 'jburkardt':
                datasetw = f'_datasets/{self.directory}/{key}_w.txt'
                datasetc = f'_datasets/{self.directory}/{key}_c.txt'
                reader = JburkardtReader(datasetw, datasetc)
            elif self.case:
                if key[0:6] == self.directory:
                    dataset = f'_datasets/binpp/{self.directory}/{key}.BPP.txt'
                    reader = BinppReader(dataset)

            if self.is_online:
                strategy: Online = self.algorithm
                result = strategy(reader.online())['solution']
            else:
                strategy: Offline = self.algorithm
                result = strategy(reader.offline())['solution']
            # print(f'{sorted(result)}')
            self.solutions[key] = len(result)  # store number of bins in solutions[key]

    # this method returns whether the solutions are optimal_solutions or not
    def discrete_margin(self) -> Discrete:
        is_optimal = {}
        if not self.case:
            for key in self.optimal.keys():  # if solution has more bins, it is_optimal = F
                if self.solutions[key] > self.optimal[key]:
                    is_optimal[key] = False
                else:
                    is_optimal[key] = True
        else:
            for key in self.optimal.keys():  # if solution has more bins, it is_optimal = F
                if key[0:6] == self.directory:
                    if self.solutions[key] > self.optimal[key]:
                        is_optimal[key] = False
                    else:
                        is_optimal[key] = True
        return is_optimal

    # this method returns how many more bins the solutions use than the optimal_solutions solution does
    def continuous_margin(self) -> Continuous:
        bin_difference = {}
        if not self.case:
            for key in self.optimal.keys():
                bin_difference[key] = self.solutions[key] - self.optimal[key]
        else:
            for key in self.optimal.keys():
                if key[0:6] == self.directory:
                    bin_difference[key] = self.solutions[key] - self.optimal[key]
        return bin_difference

    # this method displays the discrete margin
    def display_discrete(self) -> None:
        # read csv file to find optimal solutions
        self.read_csv()
        # run algorithm to find solutions
        self.run_algorithm()
        # find discrete margin
        is_optimal = self.discrete_margin()
        discrete = ''
        for key in is_optimal.keys():
            if is_optimal[key]:
                discrete += f'\n{key} is optimal'
            else:
                discrete += f'\n{key} is not optimal'
        print(discrete)

    # this method displays the continuous margin
    def display_continuous(self) -> None:
        # read csv file to find optimal solutions
        self.read_csv()
        # run algorithm to find solutions
        self.run_algorithm()
        # find continuous margin
        bin_difference = self.continuous_margin()
        title = self.algo_name
        x = []
        y = []
        for key in bin_difference.keys():
            x.append(key)
            y.append(bin_difference[key])
        plt.bar(x, y, color='maroon', width=0.5)
        plt.xlabel(f'{self.directory} data')
        plt.ylabel(f'Difference of bins from optimal solution')
        plt.title(f'Optimality of {title} Algorithm in Bin Packing {self.directory} Dataset')
        plt.show()
