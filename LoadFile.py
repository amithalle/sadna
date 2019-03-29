from DBConnection import DBConn


class FileLoader:
    def loadFile(self, path):
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
        for word in self.createWordArr(stanzas):
            conn.execStatement("insert into words (word, stanzaindex, lineGlobalindex, lineindex, wordindex) "
                               "values(?,?,?,?,?)", word)

    def createWordArr(self, stanzas):
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


a = FileLoader()
a.loadFile("testFile.txt")
for x in DBConn().select("select * from words",()):
    print x