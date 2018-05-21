from util import getDbInfo
from sqlscheme import Session
from sqlscheme import Batting
from sqlscheme import Master
from sqlscheme import Fielding
from sqlscheme import Salaries
from baseballdata import DataManager
from datavisualizer import DataVisualizer

import numpy as np


if __name__ == '__main__':
    dbInfo = getDbInfo()
    bs = Session(dbInfo)

    # salary prediction base on performance, age, team, height/weight, handedness
    # Data from salaries: year, league, team, salary
    # Data from fielding: year, position, G, InnOuts, PO, A, E, DP
    # Data from master:   weight, height, bats, throws, firstName, lastName

    salariesSql = bs.session.query(Salaries._playerID, Salaries._yearID,
                                   Salaries._lgID, Salaries._teamID, Salaries._salary).all()
    fieldingSql = bs.session.query(Fielding._playerID, Fielding._yearID, Fielding._lgID, Fielding._teamID,
                                   Fielding._stint, Fielding._POS, Fielding._G, Fielding._InnOuts,
                                   Fielding._PO, Fielding._A, Fielding._E, Fielding._DP).all()
    masterSql = bs.session.query(Master._playerID, Master._weight, Master._height, Master._bats,
                                 Master._throws, Master._nameFirst, Master._nameLast).all()
    salariesDM = DataManager(salariesSql, ['playerID', 'yearID', 'lgID', 'teamID', 'salary'])
    fieldingDM = DataManager(fieldingSql, ['playerID', 'yearID', 'lgID', 'teamID', 'stint', 'POS', 'G', 'InnOuts', 'PO', 'A', 'E', 'DP'])
    masterDM = DataManager(masterSql, ['playerID', 'weight', 'height', 'bats', 'throws', 'nameFirst', 'nameLast'])
    salariesDM.merge(fieldingDM.d, ['playerID', 'yearID', 'lgID', 'teamID'], ['playerID', 'yearID', 'lgID', 'teamID'], 'inner')
    salariesDM.merge(masterDM.d, ['playerID'], ['playerID'], 'inner')
    salariesDM.d['bats'] = salariesDM.d['bats'].map({'R': True, 'L': False})
    salariesDM.d['throws'] = salariesDM.d['throws'].map({'R': True, 'L': False})

    test, train = salariesDM.split(0.2)

    print(test[:5], train[:5])




    # orm version of inner join data. Failed.
    # foos = bs.session.query(Fielding._yearID, Fielding._lgID, Fielding._teamID, Fielding._playerID,
    #                         Master._weight, Master._height, Master._bats, Master._throws, Master._nameFirst,
    #                         Master._nameLast,
    #                         Salaries._salary).join(Salaries,
    #                                                Salaries._yearID == Fielding._yearID,
    #                                                Salaries._lgID == Fielding._lgID,
    #                                                Salaries._teamID == Fielding._teamID,
    #                                                Salaries._playerID == Fielding._playerID).join(Master,
    #                                                                                               Master._playerID == Fielding._playerID).all()



    # weight to height ratio
    # foos = bs.session.query(Master._height, Master._weight).all()
    # foos = list(filter(lambda x: not(None in x), foos))
    # foosDataManager = DataManager(foos, ['height', 'weight'])
    # dv = DataVisualizer()
    # dv.add2dScatter(foosDataManager.d['height'], foosDataManager.d['weight'])
    # dv.color = 'C3'
    # dv.alpha = 1
    # dv.add2dScatter([69, ], [196, ])
    # dv.addText(45, 180, "average height to weight ratio \nfor American male (2017) \n www.livestrong.com")
    # dv.setXLabel('height / feet')
    # dv.setYLabel('weight / pounds')
    # dv.setTitle('Baseball player height-weight ratio')
    # dv.show()



    # historical 2b, 3b, hr data
    # foos = bs.session.query(Batting._yearID, Batting._2B, Batting._3B, Batting._HR)
    # foos = list(filter(lambda element: not(None in element), foos))
    # foosDataManager = DataManager(foos, ['yearID', '2B', '3B', 'HR'])
    #
    # yearsToAvg2B = dict()
    # yearsToAvg3B = dict()
    # yearsToAvgHR = dict()
    #
    # minYear = foosDataManager.d['yearID'].min()
    # maxYear = foosDataManager.d['yearID'].max()
    # for i in range(minYear, maxYear + 1):
    #     thisYearData = foosDataManager.d.loc[foosDataManager.d['yearID'] == i]
    #     if len(thisYearData) == 0:
    #         print("year: %d relates data not found in the dataset")
    #         continue
    #     yearsToAvg2B[i] = thisYearData['2B'].sum()
    #     yearsToAvg3B[i] = thisYearData['3B'].sum()
    #     yearsToAvgHR[i] = thisYearData['HR'].sum()
    #
    # dv1 = DataVisualizer()
    # dv1.add2dPlot(list(yearsToAvg2B.keys()), list(yearsToAvg2B.values()))
    # dv1.setXLabel("year")
    # dv1.setYLabel("sum of times the batter reaches the second base")
    # dv1.setTitle("chronological order of sum of times the batter reaches the second base")
    #
    # dv2 = DataVisualizer()
    # dv2.add2dPlot(list(yearsToAvg3B.keys()), list(yearsToAvg3B.values()))
    # dv2.setXLabel("year")
    # dv2.setYLabel("sum of times the batter reaches the third base")
    # dv2.setTitle("chronological order of sum of times the batter reaches the third base")
    #
    # dv3 = DataVisualizer()
    # dv3.add2dPlot(list(yearsToAvgHR.keys()), list(yearsToAvgHR.values()))
    # dv3.setXLabel("year")
    # dv3.setYLabel("sum of times the batter successfully makes a home run")
    # dv3.setTitle("chronological order of sum of times the batter successfully makes a home run")
    #
    # dv4 = DataVisualizer()
    # dv4.add2dScatter(foosDataManager.d['yearID'], foosDataManager.d['2B'])
    # dv4.setXLabel("year")
    # dv4.setYLabel("times the batter reaches second base")
    # dv4.setTitle("chronological order of times each batter reaches the second base")
    #
    # dv5 = DataVisualizer()
    # dv5.add2dScatter(foosDataManager.d['yearID'], foosDataManager.d['3B'])
    # dv5.setXLabel("year")
    # dv5.setYLabel("times the batter successfully makes a home run")
    # dv5.setTitle("chronological order of times each batter reaches the third base")
    #
    # dv6 = DataVisualizer()
    # dv6.add2dScatter(foosDataManager.d['yearID'], foosDataManager.d['HR'])
    # dv6.setXLabel("year")
    # dv6.setYLabel("times the batter successfully makes a home run")
    # dv6.setTitle("chronological order of times each batter successfully makes a home run")
    #
    # dv1.show()

