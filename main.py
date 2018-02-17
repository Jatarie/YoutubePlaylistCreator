import praw
import time
from praw.models import MoreComments
import sys
import re
import requests
import youtube


def get_reddit_session():
    reddit = praw.Reddit(client_id="3d3fhNknZsPbXw", client_secret="Wlj_qXsqqAmyzd3Ss67X0E3ngFs",
                         user_agent="android:com.example.myredditapp:v1.2.3 (by /u/Jatariee)")
    return reddit


def parse_comment(comment, link_list):
    proper = re.findall(r'(?<=youtu).+?[a-zA-Z0-9_-]{11,12}(?=[\s\n)&]|$)', comment)
    for i in proper:
        if "watch" in i:
            i = re.findall(r'(?<=watch\?v=).+', i)[0]
        else:
            i = re.findall(r'(?<=\.be/).+', i)[0]
        link_list.append(i)
    return link_list


def main():
    reddit = get_reddit_session()
    submission = reddit.submission(id='7xmsgf')
    submission.comments.replace_more(limit=None)
    link_list = []
    for comment in submission.comments.list():
        parse_comment(comment.body, link_list)
    link_list = parse_comment(submission.selftext, link_list)
    print(link_list)
    return link_list


links = main()
youtube.request_token()
input("Press a key")
print("input accepted")
token = youtube.parse_token()
print("token function returned {}".format(token))
playlist_name = "bi-weekly music sharing thread 35"
r = youtube.create_playlist(token, playlist_name)
print("Playlist function returned {}".format(r.status_code))
playlist_id = r.json()["id"]
print("Adding links to playlist")
youtube.add_playlist_items(playlist_id, links, token)
