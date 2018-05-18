import os


def getDbInfo():
    with open("/Users/Excited/sshes/elmstreetdb.txt") as f:
        lines = f.readlines()
        assert len(lines) == 5
        #first line:    hostname
        #second line:   port
        #third line:    username
        #forth line:    passwd
        #fifth line:    dbname
        for i in range(5):
            lines[i] = lines[i].strip()
        return lines

def initEngineConnection(hostname, port, username, passwd, dbname, charset = 'GBK'):
    return 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s'%(username, passwd, hostname, port, dbname, charset)