class command:
    def __init__(self, line):
        self.line = line
        self.users = self.getUsers(line)
        self.channels = self.getChannels(line)
        self.trigger = self.getTrigger(line)
        self.reply = self.getReply(line)

    def getChannels(self, line):
        return line.split(" +", 1)[0].split(" ")

    def getUsers(self, line):
        return [item.lower() for item in line.split(" +", 1)[1].split(" -", 1)[0].split(" ")]

    def getTrigger(self, line):
        if line.split(" -", 1)[1].split(" *", 1)[0].startswith("/me"):
            return " ACTION " + (line.split(" -", 1)[1].split(" *", 1)[0])[4:len(line.split(" -", 1)[1].split(" *", 1)[0])]
        else:
            return line.split(" -", 1)[1].split(" *", 1)[0]

    def getReply(self, line):
        return line.split(" *", 1)[1].split("\n", 1)[0]
