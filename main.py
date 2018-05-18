from util import getDbInfo
from sqlscheme import BattingSession
from sqlscheme import Batting
from baseballdata import DataManager
from datavisualizer import DataVisualizer





if __name__ == '__main__':
    dbInfo = getDbInfo()
    bs = BattingSession(dbInfo)
    foos = bs.session.query(Batting).filter(Batting._playerID == 'abbotku01').all()
    





    # foos = list(filter(lambda element: not(None in element), foos))
    # foosDataManager = DataManager(foos, ['yearID', '2B', '3B', 'HR'])
    # dv = DataVisualizer()
    # dv.add2dScatter(foosDataManager.d['yearID'], foosDataManager.d['HR'])
    # dv.show()


    # dv.addLinearScatter(foosDataManager.d['2B'], 1)
    # dv.addLinearScatter(foosDataManager.d['3B'], 2)
    # dv.addLinearScatter(foosDataManager.d['HR'], 3)

