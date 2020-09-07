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

    max_song_id = DBConnection.conn().select("select max(song_id) from songs")[0][0]
    if max_song_id is None:
        max_song_id = -1

    DBConnection.conn().execStatement("insert into songs (song_id, author, create_date, song_name) values(?,?,?,?)",(max_song_id + 1, author,create_date, song_name))

    LoadFile.loadFile(word_file_name, max_song_id + 1)

    return max_song_id + 1

def prompt_for_song():
    
    song_name = input("enter song name: ")
    author = input("enter author name: ")
    create_date = input("enter create date in dd/mm/yyyy: ")
    create_date = datetime.datetime.strptime(create_date,"%d/%m/%Y")
    filename = input("enter file name: ")

    return insert_song(song_name,filename,author,create_date)

# prompt_for_song()