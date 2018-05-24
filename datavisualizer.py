from matplotlib import pyplot as plt
import pydotplus
import numpy as np
import collections

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

    def drawTreeFromDot(self, fileloc):
        graph = pydotplus.graph_from_dot_file(fileloc)
        edges = collections.defaultdict(list)
        for edge in graph.get_edge_list():
            edges[edge.get_source()].append(int(edge.get_destination()))
        for edge in edges:
            edges[edge].sort()
            for i in range(2):
                dest = graph.get_node(str(edges[edge][i]))[0]
                dest.set_fillcolor('white')
        graph.write_png('tree.png')