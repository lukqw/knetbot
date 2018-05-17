from config import NICK, PASS
import socket
import time


class bot():
    def __init__(self):
        self.lastmessage = time.time()
        self.lastwhisper = time.time()
        self.socket = socket.socket()
        print(time.ctime() + ": knetbot online")

    def conn(self):
        self.socket.connect(("irc.chat.twitch.tv", 6667))
        self.socket.send(("PASS " + PASS + "\r\n").encode("utf-8"))
        self.socket.send(("NICK " + NICK + "\r\n").encode("utf-8"))
        self.socket.send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
        print(time.ctime() + ": connected to twitch servers")

    def join(self, channel):
        self.socket.send(("JOIN #" + channel + "\r\n").encode("utf-8"))
        print(time.ctime() + ": joined #" + channel)

    def say(self, channel, message):
        if self.lastmessage <= time.time() - 1.5:
            self.lastmessage = time.time()
            if message.startswith("/"):
                self.socket.send(("PRIVMSG #" + channel + " :" + message + "\r\n").encode("utf-8"))
            else:
                self.socket.send(("PRIVMSG #" + channel + " :. " + message + "\r\n").encode("utf-8"))
            print(time.ctime() + ": sent '" + message + "' to #" + channel)

    def whisper(self, user, message):
        if self.lastwhisper <= time.time() - 1.5:
            self.lastwhisper = time.time()
            self.socket.send(("PRIVMSG #jtv :/w " + user + " " + message + "\r\n").encode("utf-8"))
            print(time.ctime() + ": whispered '" + message + "' to " + user)

    def pong(self):
        self.socket.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print(time.ctime() + ": PONG!")
