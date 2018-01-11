import MySQLdb
import functools

def getConnection():
    conn = MySQLdb.connect(
        host='localhost',
        db='scraping',
        user='mysql',
        password='mysql',
        charset='utf8mb4'
    )
    return conn

def selectColSQL(self):
    @functools.wraps(self)
    def wrpper(*args, **kwargs):
        db = getConnection()
        c = db.cursor()
        sql = 'select (%s) from cities', (self(*args, **kwargs))
        c.execute(sql)
        for i in c.fetchall():
            print(i[0])
        c.close()
        db.close()
        print("SQLClose")
        return wrpper

