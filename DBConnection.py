import sqlite3


class DBConn:

    def __init__(self):
        self.execStatement("create table if not exists words (word string, songID int , stanzaindex int,  lineindex "
                           "int, lineGlobalindex int, wordindex int)")
        self.execStatement("create table if not exists songs ( song_id int , author string,  create_date date, song_name string)")

    def openConn(self):
        self.conn = sqlite3.connect("sadnaDB")
        return self.conn

    def execStatement(self, statement, params=[]):
        self.openConn()
        self.conn.execute(statement, params)
        self.conn.commit()
        self.conn.close()

    def select(self, sql, params = []):
        self.openConn()
        results = []
        for x in self.conn.execute(sql, params):
            results.append(x)

        self.conn.close()
        return results

_private_conn = None
def conn():
    if _private_conn is None:
        _private_conn = DBConn()
    return _private_conn