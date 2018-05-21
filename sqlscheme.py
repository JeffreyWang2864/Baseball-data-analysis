import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util import initEngineConnection


orm_declarative_base = declarative_base()


class EngineManager:

    def __init__(self, engineInfo):
        self.engine = sqlalchemy.create_engine(initEngineConnection(engineInfo[0],
                                                                    engineInfo[1],
                                                                    engineInfo[2],
                                                                    engineInfo[3],
                                                                    engineInfo[4]))
        self.sessionMaker = sessionmaker(bind=self.engine)


    def getSession(self):
        return self.sessionMaker()


class Batting(orm_declarative_base):

    __tablename__ = 'batting'
    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('playerID', 'yearID', 'stint'),
        {},
    )
    sql_charset = 'GBK'
    _playerID = sqlalchemy.Column('playerID', sqlalchemy.VARCHAR(length=9), primary_key=True, nullable=False)
    _yearID = sqlalchemy.Column('yearID', sqlalchemy.Integer, primary_key=True, nullable=False)
    _stint = sqlalchemy.Column('stint', sqlalchemy.Integer, primary_key=True, nullable=False)
    _teamID = sqlalchemy.Column('teamID', sqlalchemy.VARCHAR(length=3))
    _lgID = sqlalchemy.Column('lgID', sqlalchemy.VARCHAR(length=2))
    _G = sqlalchemy.Column('G', sqlalchemy.Integer)
    _G_batting = sqlalchemy.Column('G_batting', sqlalchemy.Integer)
    _AB = sqlalchemy.Column('AB', sqlalchemy.Integer)
    _R = sqlalchemy.Column('R', sqlalchemy.Integer)
    _H = sqlalchemy.Column('H', sqlalchemy.Integer)
    _2B = sqlalchemy.Column('2B', sqlalchemy.Integer)
    _3B = sqlalchemy.Column('3B', sqlalchemy.Integer)
    _HR = sqlalchemy.Column('HR', sqlalchemy.Integer)
    _RBI = sqlalchemy.Column('RBI', sqlalchemy.Integer)
    _SB = sqlalchemy.Column('SB', sqlalchemy.Integer)
    _CS = sqlalchemy.Column('CS', sqlalchemy.Integer)
    _BB = sqlalchemy.Column('BB', sqlalchemy.Integer)
    _SO = sqlalchemy.Column('SO', sqlalchemy.Integer)
    _IBB = sqlalchemy.Column('IBB', sqlalchemy.Integer)
    _HBP = sqlalchemy.Column('HBP', sqlalchemy.Integer)
    _SH = sqlalchemy.Column('SH', sqlalchemy.Integer)
    _SF = sqlalchemy.Column('SF', sqlalchemy.Integer)
    _GIDP = sqlalchemy.Column('GIDP', sqlalchemy.Integer)
    _G_old = sqlalchemy.Column('G_old', sqlalchemy.Integer)


class Master(orm_declarative_base):

    __tablename__ = 'master'
    _playerID = sqlalchemy.Column('playerID', sqlalchemy.VARCHAR(length=10), primary_key=True, nullable=False)
    _birthYear = sqlalchemy.Column('birthYear', sqlalchemy.Integer)
    _nameFirst = sqlalchemy.Column('nameFirst', sqlalchemy.VARCHAR(length=50))
    _nameLast = sqlalchemy.Column('nameLast', sqlalchemy.VARCHAR(length=50))
    _nameGiven = sqlalchemy.Column('nameGiven', sqlalchemy.VARCHAR(length=250))
    _weight = sqlalchemy.Column('weight', sqlalchemy.Integer)
    _height = sqlalchemy.Column('height', sqlalchemy.Float)
    _bats = sqlalchemy.Column('bats', sqlalchemy.VARCHAR(length=1))
    _throws = sqlalchemy.Column('throws', sqlalchemy.VARCHAR(length=1))
    _retrolID = sqlalchemy.Column('retrolID', sqlalchemy.VARCHAR(length=9))
    _bbrefID = sqlalchemy.Column('bbrefID', sqlalchemy.VARCHAR(length=9))


class Fielding(orm_declarative_base):

    __tablename__ = 'fielding'
    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('playerID', 'yearID', 'stint', 'POS'),
        {},
    )
    _playerID = sqlalchemy.Column('playerID', sqlalchemy.VARCHAR(length=9), primary_key=True, nullable=False)
    _yearID = sqlalchemy.Column('yearID', sqlalchemy.Integer, primary_key=True, nullable=False)
    _stint = sqlalchemy.Column('stint', sqlalchemy.Integer, primary_key=True, nullable=False)
    _POS = sqlalchemy.Column('POS', sqlalchemy.VARCHAR(length=2), primary_key=True, nullable=False)
    _lgID = sqlalchemy.Column('lgID', sqlalchemy.VARCHAR(length=2))
    _teamID = sqlalchemy.Column('teamID', sqlalchemy.VARCHAR(length=3))
    _G = sqlalchemy.Column('G', sqlalchemy.Integer)
    _InnOuts = sqlalchemy.Column('InnOuts', sqlalchemy.Integer)
    _PO = sqlalchemy.Column('PO', sqlalchemy.Integer)
    _A = sqlalchemy.Column('A', sqlalchemy.Integer)
    _E = sqlalchemy.Column('E', sqlalchemy.Integer)
    _DP = sqlalchemy.Column('DP', sqlalchemy.Integer)


class Salaries(orm_declarative_base):

    __tablename__ = 'salaries'
    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('yearID', 'teamID', 'lgID', 'playerID'),
        {},
    )
    _playerID = sqlalchemy.Column('playerID', sqlalchemy.VARCHAR(length=9), primary_key=True, nullable=False)
    _yearID = sqlalchemy.Column('yearID', sqlalchemy.Integer, primary_key=True, nullable=False)
    _lgID = sqlalchemy.Column('lgID', sqlalchemy.VARCHAR(length=2), primary_key=True, nullable=False)
    _teamID = sqlalchemy.Column('teamID', sqlalchemy.VARCHAR(length=3), primary_key=True, nullable=False)
    _salary = sqlalchemy.Column('salary', sqlalchemy.Float)


class Session(object):

    def __init__(self, engineInfo):
        self.engineManager = EngineManager(engineInfo)
        self.session = self.engineManager.getSession()