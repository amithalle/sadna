import sqlite3


class DBConn:

    def __init__(self):
        self.execStatement("create table if not exists words (word string, songID int , stanzaindex int,  lineindex "
                           "int, lineGlobalindex int, wordindex int)",())

    def openConn(self):
        self.conn = sqlite3.connect("sadnaDB")
        return self.conn

    def execStatement(self, statement, params):
        self.openConn()
        self.conn.execute(statement, params)
        self.conn.commit()
        self.conn.close()

    def select(self, sql, params):
        self.openConn()
        for x in self.conn.execute(sql, params):
            yield x

        self.conn.close()
