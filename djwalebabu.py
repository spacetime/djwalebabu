import time
import generated_vlc as vlc
from slackclient import SlackClient
import json
import re
import logging

crontable = []
outputs = []
aaja_msg="Aaja {} Aaja. Tera gaana bajadun."

def should_play(msg):
    try:
        found = len(re.search('(mera+ ga+na+ baj+a+ ?do+)', msg.lower()).group(1)) > 0
    except:
        found = False
    return found

def play_song_for_user(user_info, data):
    parsed_json = json.loads(user_info)
    firstname = parsed_json['user']['name']
    if 'first_name' in parsed_json['user']['profile']:
        if len(parsed_json['user']['profile']['first_name']) > 0:
            firstname = parsed_json['user']['profile']['first_name']
    username = parsed_json['user']['name']
    outputs.append([data['channel'], aaja_msg.format(firstname)])
    mp3_path="file:///home/pi/" + username + ".mp3"
    print "Playing: " + mp3_path
#   p = vlc.MediaPlayer(mp3_path)
#   p.play()
    

def process_message(data):
    print data #logging aint working??
    sc = SlackClient(config['SLACK_TOKEN'])
    user_info = sc.api_call("users.info", user=data['user'])
    if should_play(data['text']):
        play_song_for_user(user_info, data)

