import requests

client_id = '6cbey1kwtqgule71xp3vvioe145kqv'
client_secret = '4p1s132vee7twnf30oqep7xv9a9xy6'

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)

#data output
keys = r.json()


headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + keys['access_token']
}


def isLive(streamer_name):
    stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)

    stream_data = stream.json()


    if len(stream_data['data']) == 1:
        return True
    else:
        return False