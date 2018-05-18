import pandas as pd

class DataManager:
    def __init__(self, data, columnNames):
        self.d = pd.DataFrame(data=data, index=[i for i in range(len(data))], columns=columnNames)