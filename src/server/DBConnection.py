import sqlite3


class DBConn:

    def __init__(self):
        self.execStatement("create table if not exists words (word string, songID int , stanzaindex int,  lineindex "
                           "int, lineGlobalindex int, wordindex int)")
        self.execStatement("create table if not exists songs ( song_id int , author string,  create_date date, song_name string)")
        self.execStatement("create table if not exists word_groups ( group_id int, group_name string)")
        self.execStatement("create table if not exists word_in_group ( group_id int, word string)")
        self.execStatement("create table if not exists word_relations ( relation_id int, relation_name string)")
        self.execStatement("create table if not exists word_to_word_relations ( relation_id int, first_word string, second_word string)")


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
    global _private_conn
    if _private_conn is None:
        _private_conn = DBConn()
    return _private_conn