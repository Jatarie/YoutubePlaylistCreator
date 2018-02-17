import praw
import sys
import re
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


def get_links():
    reddit = get_reddit_session()
    submission = reddit.submission(id='7xmsgf')
    submission.comments.replace_more(limit=None)
    link_list = []
    for comment in submission.comments.list():
        parse_comment(comment.body, link_list)
    link_list = parse_comment(submission.selftext, link_list)
    print(link_list)
    return link_list


links = get_links()
# youtube.request_token()
input("Press a key")
print("input accepted")
# token = youtube.parse_token()
token = 'ya29.GlxlBflLnYz9FFvUC589gBo7ZIYiRDNtd-HqvZRZlA7aRrwBu0XN5dqpkTWMIC6W-XX44S1G-XtCj36JtrcjLYa-8J4S6wCOfkJ_vzGtRTZAQ531qQHLXTRy_F-JOg'
print("token function returned {}".format(token))
topicless_link_list = []
for link in links:
    query = youtube.get_video_object(link, token)
    if query is not None:
        topicless_link = youtube.search_youtube(query, token)
        topicless_link_list.append(topicless_link)
    else:
        topicless_link_list.append(link)
links = topicless_link_list
playlist_name = "topicless bi-weekly music sharing thread 35"
r = youtube.create_playlist(token, playlist_name)
print("Playlist function returned {}".format(r.status_code))
playlist_id = r.json()["id"]
print("Adding links to playlist")
youtube.add_playlist_items(playlist_id, links, token)
