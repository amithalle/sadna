from DBConnection import conn
import itertools
import operator

def get_song_text(song_id):
    return create_text_from_words(get_song_index(song_id))

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
    line_repr = " ".join([x[0] for x in line])
    return line_repr


def get_songs_by_author(author_name):
    return conn().select("select * from songs where author = ?", [author_name])

def get_songs_by_name(song_name):
    return conn().select("select * from songs where song_name = ?", [song_name])

def get_songs_by_date_range(min, max):
    return conn().select("select * from songs where create_date between ? and ?", [min, max])

def get_song_by_words(words):
    return conn().select("select songID from words where word in (?)", [words])

# print( get_songs_by_author("amit"))
# print( get_songs_by_name("amit"))
# print( get_songs_by_date_range('2020-11-21', '2020-11-23'))

def get_word_context(word, song_id):
    occurences = conn().select("select * from words where word  = ? and songID = ?", [word, song_id])

    all_contexts = []
    for oc in occurences:
        context = conn().select("select * from words where songID = ? and lineGlobalindex between ? and ? order by lineGlobalindex asc, wordindex asc",[song_id, oc[4] - 1, oc[4] + 1])
        context_text = create_text_from_words(context)
        all_contexts.append(context_text)

    return all_contexts

def get_song_words(song_id):
    return conn().select("select distinct word from words where songID = ? order by word",[song_id])

def get_song_index(song_id):
    return conn().select("select * from words where songID = ? order by lineGlobalindex asc, wordindex asc",[song_id])

def get_word_by_global_index(song_id, line_index, word_index):
    return conn().select("select word from words where songID = ? and lineGlobalindex = ? and wordindex = ?",[song_id, line_index, word_index])

# for x in get_word_context("new",1):
#     print(x)
#     print()

# print(get_song_words(1))