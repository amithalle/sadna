from  .DBConnection import conn
from  . import get_song

def create_phrase(phrase):
    count_words = len(phrase.split(" "))
    
    max_id = conn().select("select max(phrase_id) from phrases")[0][0]
    if max_id is None:
        max_id = -1

    conn().execStatement("insert into phrases (phrase_id, phrase, length) values (%s, %s,%s)", [max_id +1, phrase, count_words])
    return max_id + 1


def get_all_phrases():
    return conn().select("select * from phrases")

def get_prhase_by_id(phrase_id):
    data = conn().select("select * from phrases where phrase_id = %s", [phrase_id])

    if len(data) > 0:
        return data[0]
    else:
        return None


def find_phrase_in_song(song_id, phrase_id):
    phrase = get_prhase_by_id(phrase_id)

    if phrase is None:
        return []
    
    occurences = conn().select("select * from (SELECT lineglobalindex, wordindex, word, group_concat (word, " ") over (order by lineglobalindex + "_" + wordindex rows %s preceding) phrase from words where songid  = %s) where phrase = %s", [phrase[2],song_id, phrase[1]])

    

# SELECT lineglobalindex, wordindex, word, group_concat (word, " ") over (order by lineglobalindex + "_" + wordindex rows  2 preceding) from words where songid = 2
