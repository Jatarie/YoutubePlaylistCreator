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
    submission = reddit.submission(id='7r7rjo')
    submission.comments.replace_more(limit=None)
    link_list = []
    for comment in submission.comments.list():
        parse_comment(comment.body, link_list)
    link_list = parse_comment(submission.selftext, link_list)
    return link_list


links = get_links()
print(len(links))
# youtube.request_token()
input("Press enter")
# token = youtube.parse_token()
token = 'ya29.GlxlBZIcMa97otw7Q6yJMP6qFUGB25RUntWl-HR2J4IfQIyRjVdpTo_iN9--YBVDrZ2wbnulBBLk2_wUBDc0GxLrrCPJ5e91nrue7JEvRVU0wk4jajUhfAguTvp-BA'
print("token function returned {}".format(token))
topicless_link_list = []

for link in links:
    query = youtube.get_video_object(link, token)
    if query is None:
        continue
    elif query is 'same':
        topicless_link_list.append(link)
    else:
        topicless_link = youtube.search_youtube(query, token)
        topicless_link_list.append(topicless_link)
        print("Before: https://youtu.be/{}\nAfter: https://youtu.be/{}".format(link, topicless_link))

links = topicless_link_list
playlist_name = "bi-weekly music sharing thread 33"
r = youtube.create_playlist(token, playlist_name)
print("Playlist function returned {}".format(r.status_code))
playlist_id = r.json()["id"]
print("Adding links to playlist")
youtube.add_playlist_items(playlist_id, links, token)
