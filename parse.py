class parse():
    def __init__(self, line, type):
        self.line = line
        self.type = type
        self.channel = self.getChannel(self.line)
        self.user = self.getUser(self.line)
        self.message = self.getMessage(self.line)

    def getChannel(self, line):
        if self.type == "message":
            return line.split(" #", 1)[1].split(" :", 1)[0]
        else:
            return "whisper"

    def getUser(self, line):
        return line.split(":", 1)[1].split("!", 1)[0]

    def getMessage(self, line):
        if "\x01ACTION" and "\x01" in line:
            return " " + (line.split(" :", 1)[1])[1:len(line.split(" :", 1)[1]) - 1]
        else:
            return line.split(" :", 1)[1]
