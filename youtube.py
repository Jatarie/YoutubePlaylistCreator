import requests
import time
import sys
import re
import google_auth_oauthlib.flow
import os


def request_token():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/youtube']
    )

    flow.redirect_uri = 'http://127.0.0.1:8000/'

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    os.startfile(authorization_url)


def parse_token():
    with open('C:\\Users\Matt\AppData\Local\Temp\log.txt-main.9444', "r") as f:
        for line in f:
            if "127.0.0.1:8000/?state=" in line:
                code_line = line
    code = re.findall(r'(?<=code=).+(?=&scope)', code_line)[0]
    r = requests.post('https://www.googleapis.com/oauth2/v4/token?code={}&client_id=671298348843-ev9ujssamatjg4j5qmic8jetc5db0udf.apps.googleusercontent.com&client_secret=TMufi3gAuuVGu-uEAe_Z4jAo&redirect_uri=http://127.0.0.1:8000/&grant_type=authorization_code'.format(code))
    token = r.json()['access_token']
    return token


def create_playlist(token, playlist_name):
    url = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet&access_token={}'
    r = requests.post(url.format(token), json={"snippet": {"title": playlist_name}})
    return r


def add_playlist_items(playlist_id, links, token):
    url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&access_token={}'
    for index, link in enumerate(links):
        sys.stdout.write("\r{}/{}".format(index, len(links)))
        r = requests.post(url.format(token), json={
                "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": link
                }}})
        if r.status_code != 200:
            print()
            print(r.status_code, link)
            print()


def get_video_object(link, token):
    r = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&id={}&access_token={}'.format(link, token))
    title = re.findall(r'(?<=title":\s").+(?=",)', r.text)[0]
    channel = re.findall(r'(?<=channelTitle":\s").+(?=",)', r.text)[0]
    if "- Topic" in channel:
        artist = re.findall(r'.+(?= - Topic)', channel)[0]
        query = (artist + "+" + title).replace(" ", "+")
        query = query.replace('?', '')
        return query


def search_youtube(query, token):
    r = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={}&type=video&access_token={}'.format(query, token))
    time.sleep(0.1)
    video_id = re.findall(r'(?<=videoId":\s").+(?=")', r.text)[0]
    return video_id
