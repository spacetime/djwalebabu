import time
import generated_vlc as vlc
from slackclient import SlackClient
import json
import re
import logging
import os.path

crontable = []
outputs = []

class DjWaleBabu:
    aaja_msg = "Aaja {} Aaja. Tera gaana bajadun."
    not_playing = "Baby, gaana bajaane to de"
    stop_playback = "Toot gaya sandal?"
    already_playing = "Firse bajadun?"

    vlc_player = None

    def can_play(self, msg):
        try:
            found = len(re.search('(mera+ ga+na+ baj+a+ ?do+)', msg.lower()).group(1)) > 0
        except:
            found = False
        return found

    def can_stop(self, msg):
        try:
            found = len(re.search('(chup karo?)', msg.lower()).group(1)) > 0
        except:
            found = False
        return found

    def play_song_for_user(self, user_info, data):
        if self.vlc_player is not None and self.vlc_player.is_playing():
            outputs.append([data['channel'], self.already_playing])
            return
        parsed_json = json.loads(user_info)
        firstname = parsed_json['user']['name']
        if 'first_name' in parsed_json['user']['profile']:
            if len(parsed_json['user']['profile']['first_name']) > 0:
                firstname = parsed_json['user']['profile']['first_name']
        username = parsed_json['user']['name']
        outputs.append([data['channel'], self.aaja_msg.format(firstname)])
        mp3_path="file:///home/pi/" + username + ".mp3"
        if not os.path.isfile(mp3_path):
            mp3_path="file:///home/pi/" + "default.mp3"
        print "Playing: " + mp3_path
        self.vlc_player = vlc.MediaPlayer(mp3_path)
        self.vlc_player.play()

    def stop_song(self, data):
        print self.vlc_player
        if self.vlc_player is None or not self.vlc_player.is_playing():
            outputs.append([data['channel'], self.not_playing])
        else:
            outputs.append([data['channel'], self.stop_playback])
            self.vlc_player.stop()

babu = DjWaleBabu()

def process_message(data):
    print data #logging aint working??
    sc = SlackClient(config['SLACK_TOKEN'])
    if babu.can_play(data['text']):
        user_info = sc.api_call("users.info", user=data['user'])
        babu.play_song_for_user(user_info, data)
    if babu.can_stop(data['text']):
        babu.stop_song(data)
