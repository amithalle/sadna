from  .DBConnection import conn
from  . import get_song


def get_word_relation(relation_id):
    return conn().select("select * from word_relations where relation_id = ?", [relation_id])

def create_relation(relation_name):
    max_relation_id = conn().select("select max(relation_id) from word_relations")[0][0]
    if max_relation_id is None:
        max_relation_id = -1

    relation_id = max_relation_id +1

    conn().execStatement("insert into word_relations values(%s,%s)", [relation_id, relation_name])
    return  relation_id

def get_word_relations():
    return conn().select("select * from word_groups")

def add_word_relation(words, relation_id):
    conn().execStatement("insert into word_to_word_relations values(%s,%s,%s)", [relation_id, *words])