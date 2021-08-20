import xml.etree.ElementTree as ET
from . import get_song, word_groups, create_song, phrases, LoadFile

SONG = "song"
PHRASE = "phrase"
WORD_GROUP = "word_group"

def get_base_xml():
    return ET.Element("data")

def dump_song(song):
    elem = ET.Element(SONG, attrib=row2dict(song))
    words = get_song.get_words_for_song(song["song_id"])
    for word in words:
        elem.append(dump_word(word))
    return elem


def dump_word(word):
    elem = ET.Element("word", attrib=row2dict(word))
    return elem


def dump_phrase(phrase):
    elem = ET.Element(WORD_GROUP, attrib=row2dict(phrase))
    return elem

def dump_word_group(word_group):
    elem = ET.Element(WORD_GROUP, attrib=row2dict(word_group))

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


def import_song(song_xml):
    author = song_xml.get("author")
    name = song_xml.get("song_name")
    create_date = song_xml.get("create_date")
    song_id = create_song.insert_song_metadata(name, author, create_date)

    for word in song_xml.getchildren():
        import_word_in_song(word, song_id)
    return song_id


def import_word_in_song(word_xml, song_id):
    word = word_xml.get("word")
    stanzaindex = word_xml.get("stanzaindex")
    lineindex = word_xml.get("lineindex")
    lineGlobalindex = word_xml.get("lineGlobalindex")
    wordindex = word_xml.get("wordindex")
    LoadFile.insert_word_in_song(song_id, word, stanzaindex, lineGlobalindex, lineindex, wordindex)

def import_phrase(phrase_xml):
    phrase = phrase_xml.get("phrase")
    phrases.create_phrase(phrase)


def import_word_group(word_group_xml):
    group_name = word_group_xml.get("group_name")
    words = [word.text for word in word_group_xml.find("words").getchildren()]
    word_groups.create_word_group(group_name, words)

def read_imported_file(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    for child in root.getchildren():
        if child.tag == SONG:
            import_song(child)
        elif child.tag == PHRASE:
            import_phrase(child)
        elif child.tag == WORD_GROUP:
            import_word_group(child)
        else:
            raise Exception("tag is not suppprted:" + child.tag)