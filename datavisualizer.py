from matplotlib import pyplot as plt
import numpy as np

class DataVisualizer:
    def __init__(self):
        self.p = plt.figure()
        self.figure = self.p.add_subplot(111)

    def add1dScatter(self, data, at):
        data = np.array((data, [at] * len(data)))
        self.figure.scatter(data[1], data[0], marker='o', alpha=0.05)

    def add2dScatter(self, xs, ys):
        self.figure.scatter(xs, ys, marker='o', alpha=0.05)

    def show(self):
        plt.show()
