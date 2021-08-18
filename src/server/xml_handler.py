import xml.etree.ElementTree as ET
from . import get_song

def get_base_xml():
    return ET.Element("data")


def dump_song(song):
    elem = ET.Element("song", attrib=row2dict(song))
    words = get_song.get_words_for_song(song["song_id"])
    for word in words:
        elem.append(dump_word(word))
    return elem


def dump_word(word):
    elem = ET.Element("word", attrib=row2dict(word))
    return elem

# print(ET.tostring(dump_song({"songID": "1"})))

def row2dict(row):
    d = {}
    for k in row.keys():
        d[k] = str(row[k])
    return d


def to_string(element):
    s = ET.tostring(element)

    return str(s, 'utf-8')