import xml.etree.ElementTree as ET
from . import get_song, word_groups

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


def dump_phrase(phrase):
    elem = ET.Element("phrase", attrib=row2dict(phrase))
    return elem

def dump_word_group(word_group):
    elem = ET.Element("word_group", attrib=row2dict(word_group))

    # add all the words in the group
    words = word_groups.get_words_in_group(word_group["group_id"])
    words_arr = ET.Element("words")
    for word in words:
        word_elem =ET.Element("word")
        word_elem.text = str(word)
        words_arr.append(word_elem)

    elem.append(words_arr)
    return elem

def row2dict(row):
    d = {}
    for k in row.keys():
        d[k] = str(row[k])
    return d


def to_string(element):
    s = ET.tostring(element, encoding="unicode")

    return s