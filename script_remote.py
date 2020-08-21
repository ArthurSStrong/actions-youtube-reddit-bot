"""Takes the last 3 user videos and posts them to Reddit."""
import os
import praw
import requests


CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

_KEY = os.environ["_KEY"]


LOG_FILE = "./processed_ids.txt"


def load_log():
    """Loads the log file and creates it if it doesn't exist.

    Returns
    -------
    list
        A list of ids.

    """

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as temp_file:
            return temp_file.read().splitlines()

    except Exception:
        with open(LOG_FILE, "w", encoding="utf-8") as temp_file:
            return []


def update_log(video_id):
    """Updates the log file.

    Parameters
    ----------
    video_id : str
        The video_id to log.

    """

    with open(LOG_FILE, "a", encoding="utf-8") as temp_file:
        temp_file.write(video_id + "\n")


def get_channel_items(channel):
    """Gets videos from api.

    Returns
    -------
    list
        A list of videos elements.

    """
    api_url = "https://www.googleapis.com/youtube/v3/search?channelId={}&part=snippet&maxResults=3&order=date&key={}".format(channel, _KEY)
    try:
        with requests.get(api_url) as response:
            print("request OK")
            data = response.json()
            return data['items']
    except:
        print("Error during request")
        exit()


def init_bot():
    """Reads the RSS feed."""

    # We create the Reddit instance.
    reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=USERNAME, password=PASSWORD, user_agent="testscript by /u/larry3000bot")

    # Get videos from youtube api
    channel_id = 'UCwi7FK3XDDwhioq1hV8Zmqg'
    videos = get_channel_items(channel_id)
    logged_ids = load_log()

    for video in videos:
        if video['id']['videoId'] not in logged_ids:
            video_url = "https://www.youtube.com/watch?v="+video['id']['videoId']
            title = video['snippet']['title']
            reddit.subreddit('lazonacero').submit(
                    title=title, url=video_url)
            update_log(video['id']['videoId'])

    print("end of script")


if __name__ == "__main__":

    init_bot()
