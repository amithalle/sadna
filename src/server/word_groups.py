from  .DBConnection import conn
from  . import get_song

def create_word_group(group_name, words):
    max_group_id = conn().select("select max(group_id) from word_groups")[0][0]
    if max_group_id is None:
        max_group_id = -1

    group_id = max_group_id +1

    conn().execStatement("insert into word_groups (group_id, group_name) values(?,?)",[group_id, group_name])

    add_words_to_group(group_id, words)
    return group_id

# create_word_group("amit", ["amit", "hello"])


def get_groups():
    return conn().select("select * from word_groups")

def get_group_name(id):
    return conn().select("select group_name from word_groups where group_id = ?", [id])


def add_words_to_group(group_id, words):
    for word in words:
        try:
            conn().execStatement("insert into word_in_group (group_id, word) values(?,?)",[group_id, word])
        except:
            # ingore duplicates
            pass

def get_words_in_group(group_id):
    return [x[0] for x in conn().select("select word from word_in_group where group_id = ?", [group_id])]

# print(get_words_in_group(0))

def get_songs_by_group(group_id):
    return get_song.get_song_by_words(get_words_in_group(group_id))


