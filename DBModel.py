# -*- encoding:utf-8 -*-

import MySQLdb
import functools

DB_NAME = 'scraping'

DATABASE = {
    "host": "localhost",
    "db": DB_NAME,
    "user": "mysql",
    "password": "mysql",
    "charset": "utf8mb4"
}

class DB():
    def get_connection(self):
        self.db = MySQLdb.connect(**DATABASE)
        return self.db

    def close_connection(self):
        if self.db is not None:
            self.db.close()

# def DB_Connection_Wrpper(self):
#     @functools.wraps(self)
#     def wrpper(*args, **kwargs):
#         db = DB()
#         cur = db.get_connection().cursor()
#         sql = 'select (%s) from cities', (self(*args, **kwargs))
#         cur.execute(sql)
#         db.close_connection()
#         print("SQL_Wrapper")
#         return wrpper

class Exists_Tables():
    def __init__(self):
        self.db = DB()

    def Execute_SQL(self, sql):
        try:
            cur = self.db.get_connection().cursor()
            cur.execute(sql)
            self.db.close_connection()
            return True
        except:
            return False

    def exists_create_user(self):
        try:
            sql = '''
                CREATE TABLE IF NOT EXISTS user(
                id INT(11) PRIMARY KEY AUTO_INCREMENT,
                user_name VARCHAR(24) UNIQUE NOT NULL,
                user_pass VARCHAR(24) NOT NULL,
                creation_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                modification_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            '''
            self.Execute_SQL(sql)
            return True
        except:
            return False


class DB_Controller():
    def __init__(self):
        self.db = DB()

    def insert_user(self, user_name, user_pass):
        try:
            db = self.db.get_connection()
            cur = db.cursor()
            sql = '''INSERT INTO user (user_name, user_pass) VALUES (%s, %s)'''
            cur.execute(sql, (user_name, user_pass))
            db.commit()
            self.db.close_connection()
            recode = self.select_user(user_name, user_pass)
            return recode
        except:
            return None

    def select_user(self, user_name, user_pass=None):
        try:
            if user_pass is None:
                print('')

            else:
                cur = self.db.get_connection().cursor()
                sql = 'SELECT user_name FROM user WHERE user_name = (%(user_name)s) AND user_pass = (%(user_pass)s)'
                cur.execute(sql, {'user_name': user_name, 'user_pass': user_pass})
                recode = cur._rows[0][0]
                self.db.close_connection()
                return recode
        except:
            return None



# c = conn.cursor()   # カーソルを取得する
# # execute()メソッドでSQL文を実行する
# # このスクリプトを何回実行しても同じ結果になるようにするため、citiesテーブルが存在する場合は削除する。
# # c.execute('''
# #     DROP TABLE scraping
# # ''')
# c.execute('''
#     CREATE TABLE scraping.cities (
#         rank integer,
#         city text,
#         population integer
#     )
#     ''')
# print('終了')
#
# # execute()メソッドの第2引数にはSQL文のパラメータを指定できる。
# # パラメーターで置き換える場所(プレースホルダー)は%sで指定する。
# c.execute('INSERT INTO cities VALUES (%s, %s, %s)', (1, '上海', 2415000))
# conn.commit()   # 変更をコミット(保存)する。
#
# c.execute('INSERT INTO cities VALUES (%s, %s, %s)', (1, '上海', 2415000))
# conn.commit()   # 変更をコミット(保存)する。
#
#
# # パラメーターが辞書の場合、プレースホルダーは %(名前)s で指定する。
# c.execute('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)',
#           {'rank': 2, 'city': 'カラチ', 'population': 2350000})
#
# # executemany()メソッドでは、複数のパラメーターをリストで指定し、複数(ここでは3つ)のSQL文を実行する。
# data = []
# data = {'rank': 3, 'city': '北京', 'population': 21516000},
# {'rank': 4, 'city': '天津', 'population':147221000},
# {'rank': 5, 'city': 'インスタブル', 'population':14160467},
# c.executemany('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)', [
# {'rank': 3, 'city': '北京', 'population': 21516000},
# {'rank': 4, 'city': '天津', 'population': 147221000},
# {'rank': 5, 'city': 'インスタブル', 'population': 14160467},
# ])
#
# conn.commit()   # 変更をコミット(保存)する。
#
# c.execute('SELECT * FROM cities')   # 保存したデータを取得する。
# for row in c.fetchall():    # クエリの結果はfetchall()メソッドで取得できる。
#     print(row)  # 取得したデータを表示する
#
# conn.close()    # コネクションを閉じる
