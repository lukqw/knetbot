from config import CHAN, BOTS, ADMIN
from command import *
from parse import *
from bot import *
from threading import Thread
import sys


class run():
    def __init__(self):
        self.bot = bot()
        self.bot.conn()
        self.commandlist = self.getcommands()
        for chan in CHAN:
            self.bot.join(chan)
        self.counterjoin = [0] * len(CHAN)

    def listen(self):
        while True:
            buffer = (self.bot.socket.recv(4096)).decode("utf-8", errors="ignore")
            temp = buffer.split("\r\n")
            buffer = temp.pop()

            for line in temp:

                if "PRIVMSG" in line:
                    try:
                        par = parse(line, "message")
                        print(time.ctime() + ": #" + par.channel + ": " + par.user + " wrote '" + par.message + "'")

                        if "!join" in par.message:
                            self.counterjoin[CHAN.index(par.channel)] += 1
                            if self.counterjoin[CHAN.index(par.channel)] > 20:
                                self.bot.say(par.channel, "!join KKona")
                                self.counterjoin[CHAN.index(par.channel)] = 0

                        if par.message.startswith("!quit"):
                            if par.user in ADMIN:
                                self.bot.say(par.channel, "shutting down master MrDestructoid")
                                sys.exit()

                        if par.message.startswith("!addcomm"):
                            if par.user in ADMIN:
                                try:
                                    self.addcomm(par)
                                except:
                                    self.bot.say(par.channel, "error adding command")

                        if par.message.startswith("!delcomm"):
                            if par.user in ADMIN:
                                try:
                                    self.delcomm(par)
                                except:
                                    self.bot.say(par.channel, "error deleting command")

                        if par.message.startswith("!kommands"):
                            co = "!kommands for " + par.user + ": "
                            for comms in self.commandlist:
                                if (par.channel in comms.channels) or comms.channels[0] == "all":
                                    if (comms.trigger not in co) and ((par.user in comms.users) or comms.users[0] == "all"):
                                        co += comms.trigger + ", "
                            self.bot.say(par.channel, co[0:len(co) - 2])

                        if par.message.startswith("!chat"):
                            usedbot = par.message.split(" #", 1)[1].split(" ")[0]
                            if NICK == usedbot:
                                channel123 = par.message.split(" +", 1)[1].split(" ")[0]
                                message123 = par.message.split(" -", 1)[1]
                                self.bot.join(channel123)
                                self.bot.say(channel123, message123) 

                        for comm in self.commandlist:
                            if par.message.startswith(comm.trigger + " ") or par.message == comm.trigger:
                                if (par.channel in comm.channels) or comm.channels[0] == "all":
                                    if (par.user in comm.users) or comm.users[0] == "all":
                                        self.bot.say(par.channel, comm.reply)

                    except SystemExit:
                        sys.exit()

                    except:
                        print(time.ctime() + ": error parsing/printing message")

                elif "WHISPER" in line:
                    try:
                        par = parse(line, "whisper")
                        print(time.ctime() + ": #" + par.channel + ": " + par.user + " wrote '" + par.message + "'")

                        if par.user in ADMIN:
                            self.bot.whisper(par.user, "test")

                    except:
                        print(time.ctime() + ": error parsing/printing whisper")

                elif "PING" in line:
                    print(time.ctime() + ": PING!")
                    self.bot.pong()

                else:
                    try:
                        print(time.ctime() + ": " + line)
                    except:
                        print(time.ctime() + ": error printing *other* line")

            sys.stdout.flush()

    def getcommands(self):
        commands = []
        with open("commlist.txt") as f:
            for line in f.readlines():
                if line != "\n":
                    commands.append(command(line))
            print(time.ctime() + ": successfully read commandlist")
        return commands

    def addcomm(self, addparse):
        line = addparse.message.split(" ", 1)[1]
        comm = command(line)

        freecomm = True

        for commands in self.commandlist:
            freetrigger = True
            freechannel = True
            freeuser = True
            if comm.trigger == commands.trigger:
                freetrigger = False
                for chan in comm.channels:
                    if chan in commands.channels:
                        freechannel = False
                for user in comm.users:
                    if user in commands.users:
                        freeuser = False
            if not freetrigger and not freechannel and not freeuser:
                freecomm = False

        if freecomm:
            self.commandlist.append(comm)
            self.bot.say(addparse.channel, "added command: " + comm.trigger)

            with open("commlist.txt", "r+") as f:
                data = f.read()
                f.seek(0)
                f.write(data + "\n" + line)
                f.truncate()

        else:
            self.bot.say(addparse.channel, "command already in use: " + comm.trigger)

    def delcomm(self, delparse):
        line = delparse.message.split(" ", 1)[1]
        comm = command(line)

        for commands in self.commandlist:
            usedtrigger = False
            usedchannel = False
            useduser = False

            if comm.trigger == commands.trigger:
                usedtrigger = True
                for chan in comm.channels:
                    if chan in commands.channels:
                        usedchannel = True
                for user in comm.users:
                    if user in commands.users:
                        useduser = True

            if usedtrigger and usedchannel and useduser:
                self.commandlist.remove(commands)
                self.bot.say(delparse.channel, "deleted command: " + comm.trigger)

                txt = ""
                for comm in self.commandlist:
                    txt += comm.line + "\n"

                print(txt)
                f = open("commlist.txt", "w")
                f.write(txt)
                f.close()
                return


run = run()
Thread(target=run.listen).start()
