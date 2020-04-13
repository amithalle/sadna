from DBConnection import DBConn


def loadFile( path, song_id):
    stanzas = []
    with open(path, "r") as file:
        lines = file.readlines()

        while "\n" in lines:
            stanzas.append(lines[:lines.index("\n")])
            lines = lines[lines.index("\n") + 1:]

    if len(lines) != 0:
        stanzas.append(lines)
    # print stanzas
    # print self.createWordArr(stanzas)
    #
    conn = DBConn()
    for word in createWordArr(stanzas):
        conn.execStatement("insert into words (word, stanzaindex, lineGlobalindex, lineindex, wordindex, songID) "
                            "values(?,?,?,?,?,?)", (*word, song_id))

def createWordArr(stanzas):
    words = []
    index_stanza = 0
    index_global_line = 0
    for stanza in stanzas:
        index_line = 0
        for line in stanza:
            index_word = 0
            for word in line.split():
                words.append((word, index_stanza, index_global_line, index_line, index_word))
                index_word += 1

            index_line += 1
            index_global_line += 1

        index_stanza += 1

    return words


# loadFile("testFile.txt")
# for x in DBConn().select("select * from words",()):
#     print (x)