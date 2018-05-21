import pandas as pd
import numpy as np

class DataManager:
    def __init__(self, data, columnNames):
        self.d = pd.DataFrame(data=data, index=[i for i in range(len(data))], columns=columnNames)

    def merge(self, right, left_on, right_on, how):
        self.d = self.d.merge(right=right, how=how, left_on=left_on, right_on=right_on)

    def split(self, testingPortion):
        assert 0 < testingPortion < 1
        msk = np.random.rand(len(self.d)) < testingPortion
        return self.d[msk], self.d[~msk]