from . import LoadFile
from . import DBConnection
import os
import datetime

def insert_song(song_name, word_file_name, author, create_date):
    """get a song and put to DB
    
    Arguments:
        song_name {String} -- the song name
        word_file_name {String} -- the file name
        author {String} -- author's name
        create_date {Date} -- the date the wond was written
    
    Raises:
        Exception: invalid input
    """
    # test the file
    if not word_file_name.endswith('.txt') or word_file_name == '.txt':
        raise Exception("invalid file name")

    if not os.path.isfile(word_file_name):
        raise Exception("file not exists")

    song_id = insert_song_metadata(song_name, author, create_date)

    LoadFile.loadFile(word_file_name, song_id)


def insert_song_metadata(song_name, author, create_date):
    max_song_id = DBConnection.conn().select("select max(song_id) from songs")[0][0]
    if max_song_id is None:
        max_song_id = -1

    DBConnection.conn().execStatement("insert into songs (song_id, author, create_date, song_name) values(?,?,?,?)",(max_song_id + 1, author,create_date, song_name))
    return max_song_id + 1
