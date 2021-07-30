from .DBConnection import conn
import itertools
import operator

def get_song_text(song_id):
    return create_text_from_words(get_words_for_song(song_id))

def create_text_from_words(words):
    stanzas = []
    for _,g in itertools.groupby(words,operator.itemgetter(2)):
        stanzas.append(list(g))
    
    pass
    return "\n\n".join([generate_stanza(x) for x in stanzas])


def generate_stanza(stanza):
    lines = []
    for _,g in itertools.groupby(stanza,operator.itemgetter(3)):
        lines.append(list(g))

    stanza_repr =  "\n".join([generate_line(x) for x in lines])
    return stanza_repr

def generate_line(line):
    line_repr = " ".join([str(x[0]) for x in line])
    return line_repr

def get_all_songs():
    return conn().select("select * from songs")

def get_songs_by_author(author_name):
    return conn().select("select * from songs where author = ?", [author_name])

def get_songs_by_name(song_name):
    return conn().select("select * from songs where song_name = ?", [song_name])

def get_songs_by_date_range(min, max):
    return conn().select("select * from songs where create_date between ? and ?", [min, max])

def get_song_ids_by_words(words):
    if len(words) == 0:
        return []
    # sqlite3 doesn;t support array parameter
    param_arr = ",".join(["?" for x in range (len(words))])
    return [x[0] for x in conn().select("select songID from words where word in ({})".format(param_arr), words)]


def get_songs_by_id(id_list):
    if len(id_list) == 0:
        return []
    param_arr = ",".join(["?" for x in range (len(id_list))])
    return conn().select("select * from songs where song_id in ({})".format(param_arr), id_list)



# print( get_songs_by_author("amit"))
# print( get_songs_by_name("amit"))
# print( get_songs_by_date_range('2020-11-21', '2020-11-23'))

def get_word_context(word, song_id=None):
    word_condition= ""
    song_condition = ""
    params = []
    if isinstance(word, (list, tuple)):
        param_arr = ",".join(["?" for x in range (len(word))])

        word_condition = "word in ({})".format(param_arr)
        [params.append(x) for x in word]
    else:
        word_condition = "word = ?"
        params.append(word)
    
    if song_id is not None:

        if isinstance(song_id, (list, tuple)):
            param_arr = ",".join(["?" for x in range (len(song_id))])
            song_condition = "and songID in ({})".format(param_arr)
            [params.append(x) for x in song_id]

        else:
            song_condition = "and songID = ?"
            params.append(song_id)

    occurences = conn().select("select * from words where {} {}".format(word_condition, song_condition), params=params)

    all_contexts = []
    for oc in occurences:
        all_contexts.append(get_line_context(oc[1],oc[4]))

    return all_contexts

def get_song_words(song_id):
    return conn().select("select word, count(*) as cnt from words where songID = ? group by word",[song_id])

def get_all_words():
    return conn().select("select word, count(*) as cnt from words group by word")


def get_words_for_song(song_id):
    return conn().select("select * from words where songID = ? order by lineGlobalindex asc, wordindex asc",[song_id])

def get_word_by_global_index(song_id, line_index, word_index):
    return conn().select("select word from words where songID = ? and lineGlobalindex = ? and wordindex = ?",[song_id, line_index, word_index])

def get_word_by_stanza_index(song_id, stanza_index, line_index, word_index):
    return conn().select("select word from words where songID = ? and stanzaindex =? and lineindex = ? and wordindex = ?",[song_id, stanza_index, line_index, word_index])


def get_line_context(song_id, lineglobal_index):
    context = conn().select("select * from words where songID = ? and lineGlobalindex between ? and ? order by lineGlobalindex asc, wordindex asc",[song_id, lineglobal_index -1, lineglobal_index +1])
    return {"text": create_text_from_words(context), "song_id": song_id} 


# for x in get_word_context("new",1):
#     print(x)
#     print()

# print(get_song_words(1))