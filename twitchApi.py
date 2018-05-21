
import json
import urllib
from config import CHAN, BOTS, ADMIN
from command import *
from parse import *
from bot import *

class twitch_api():

    def __init__(self, streamer):
        self.client_id = self.getClientID()
        self.api_response = self.getTwitchApi(streamer)
        self.game_id = self.api_response['data'][0]['game_id']
        self.stream_id = self.api_response['data'][0]['id']
        self.stream_lang = self.api_response['data'][0]['language']
        self.stream_started_at = self.api_response['data'][0]['started_at']
        self.stream_title = self.api_response['data'][0]['title']
        self.stream_type = self.api_response['data'][0]['type']
        self.broadcaster_id = self.api_response['data'][0]['user_id']
        self.viewers = self.api_response['data'][0]['viewer_count']


    def getTwitchApi(self, target_channel):
        url_userlogin = "https://api.twitch.tv/helix/streams?user_login=" + target_channel
        req_userlogin = urllib.request.Request(url_userlogin)
        req_userlogin.add_header("Client-ID", self.getClientID())
        req_userlogin.add_header("Authorization", "OAuth " + PASS[6:])
        html_response = urllib.request.urlopen(req_userlogin).read().decode("UTF-8")
        html_response = json.loads(html_response)

        return html_response

    def getClientID(self):
        url = "https://id.twitch.tv/oauth2/validate"
        req = urllib.request.Request(url)
        req.add_header("Authorization", "OAuth " + PASS[6:])
        contents = urllib.request.urlopen(req)
        return contents.read()[14:45]
