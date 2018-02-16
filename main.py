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
    links = re.findall(r'http.+?(?=\))', comment)
    for link in links:
        if "spotify" not in link:
            try:
                x = re.findall(r'(?<=youtu.be/).+', link)[0][0:12]
            except:
                try:
                    x = re.findall(r'(?<=watch\?v=).+', link)[0][0:12]
                except IndexError:
                    continue
            if x[-1] == "&":
                x = x[:-1]
            link_list.append(x)
    return link_list


def main():
    reddit = get_reddit_session()
    submission = reddit.submission(id='7xmsgf')
    submission.comments.replace_more(limit=None)
    link_list = []
    for comment in submission.comments.list():
        link_list = parse_comment(comment.body, link_list)
    link_list = parse_comment(submission.selftext, link_list)
    return link_list


links = main()
youtube.request_token()
input("Press a key")
token = youtube.parse_token()
playlist_name = "bi-weekly music sharing thread 35"
r = youtube.create_playlist(token, playlist_name)
playlist_id = r.json()["id"]
youtube.add_playlist_items(playlist_id, links, token)
