from util import getDbInfo
from sqlscheme import Session
from sqlscheme import Batting
from sqlscheme import Master
from sqlscheme import Appearances
from sqlscheme import Salaries
from baseballdata import DataManager
from datavisualizer import DataVisualizer
from sklearn import tree
from sklearn import linear_model
from sklearn import metrics

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
    appearancesSql = bs.session.query(Appearances._playerID, Appearances._yearID, Appearances._lgID, Appearances._teamID,
                                      Appearances._G_all, Appearances._GS, Appearances._G_batting,
                                      Appearances._G_defense, Appearances._G_p, Appearances._G_c,
                                      Appearances._G_1b, Appearances._G_2b, Appearances._G_3b,
                                      Appearances._G_ss, Appearances._G_lf, Appearances._G_cf,
                                      Appearances._G_rf, Appearances._G_of).all()
    masterSql = bs.session.query(Master._playerID, Master._weight, Master._height, Master._bats,
                                 Master._throws, Master._nameFirst, Master._nameLast).all()
    salariesDM = DataManager(salariesSql, ['playerID', 'yearID', 'lgID', 'teamID', 'salary'])
    appearancesDM = DataManager(appearancesSql, ['playerID', 'yearID', 'lgID', 'teamID', 'G_all', 'G_GS', 'G_batting',
                                                 'G_defense', 'G_p', 'G_c', 'G_1b', 'G_2b', 'G_3b', 'G_ss', 'G_lf',
                                                 'G_cf', 'G_rf', 'G_of'])
    maxYear = appearancesDM.d['yearID'].max()
    deletingIndexes = list()
    for index, row in appearancesDM.d.iterrows():
        if index == maxYear:
            deletingIndexes.append(index)
            continue
        appearancesDM.d.at[index, 'yearID'] = appearancesDM.d.at[index, 'yearID'] + 1
    appearancesDM.d.drop(deletingIndexes)
    masterDM = DataManager(masterSql, ['playerID', 'weight', 'height', 'bats', 'throws', 'nameFirst', 'nameLast'])
    salariesDM.merge(appearancesDM.d, ['playerID', 'yearID', 'lgID', 'teamID'], ['playerID', 'yearID', 'lgID', 'teamID'], 'inner')
    salariesDM.merge(masterDM.d, ['playerID'], ['playerID'], 'inner')
    #salariesDM.d = salariesDM.d.loc[:, salariesDM.d.columns != 'playerID']
    salariesDM.d = salariesDM.d[['yearID', 'lgID', 'teamID', 'salary', 'bats', 'throws', 'G_all', 'G_GS', 'G_batting',
                                                 'G_defense']]
    salariesDM.d['bats'] = salariesDM.d['bats'].map({'R': True, 'L': False})
    salariesDM.d['throws'] = salariesDM.d['throws'].map({'R': True, 'L': False})
    salariesDM.dropna()
    salariesDM.convertString(['lgID', 'teamID'])
    res = 0
    while abs(res) < 0.6:
        test, train = salariesDM.split(0.1)
        trainY = train['salary']
        trainX = train.drop('salary', axis=1)
        testY = test['salary']
        testX = test.drop('salary', axis=1)
        clf = tree.DecisionTreeRegressor()
        clf.fit(trainX, trainY)
        #   [ 131731.88188759  542168.95388081   -5251.10564173  136570.37851864
        #   -319313.29760229   27511.55882623   45128.46481922  -44551.27638958
        #   -9151.56213622]
        predictedY = clf.predict(testX)
        res = metrics.r2_score(testY, predictedY)
        print(res)

    with open("/Users/Excited/PycharmProjects/Baseball-data-analysis/result.txt", 'w') as f:
        f.write("r_square: %.6f\n"%res)
        f.write("\npredict results:\n========================================\n")
        for a, b in zip(predictedY, testY):
            f.write("predict: %f\tactual: %f\n"%(a, b))
        predictedY = [sum(predictedY[i*20:i*20+20]) for i in range(len(predictedY)//20)]
        testY = [sum(testY[i*20:i*20+20]) for i in range(len(testY)//20)]
        vv = DataVisualizer()
        vv.setXLabel("number of samples * 50")
        vv.setYLabel("sum of every 50 samples")
        vv.setTitle("comparison of predicted salary and real salary for sum of every 50 samples")
        vv.alpha=1.0
        vv.add2dPlot([i for i in range(1, len(predictedY) + 1)], predictedY)
        vv.color = 'C2'
        vv.add2dPlot([i for i in range(1, len(testY) + 1)], testY)
        vv.show()





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

