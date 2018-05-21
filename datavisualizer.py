from matplotlib import pyplot as plt
import numpy as np

class DataVisualizer:
    def __init__(self):
        self.p = plt.figure()
        self.figure = self.p.add_subplot(111)
        self.color = 'C0'
        self.alpha = 0.05

    def add1dScatter(self, data, at):
        data = np.array((data, [at] * len(data)))
        self.figure.scatter(data[1], data[0], marker='o', alpha=self.alpha, c=self.color)

    def add2dScatter(self, xs, ys):
        self.figure.scatter(xs, ys, marker='o', alpha=self.alpha, c=self.color)

    def add2dPlot(self, xs, ys):
        self.figure.plot(xs, ys, alpha=self.alpha, c=self.color)

    def setXLabel(self, label):
        plt.xlabel(label)

    def setYLabel(self, label):
        plt.ylabel(label)

    def setTitle(self, title):
        plt.title(title)

    def addText(self, x, y, string):
        self.figure.text(x, y, string)

    def show(self):
        plt.show()
