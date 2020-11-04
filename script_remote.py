#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Takes the last 3 user videos from channels and posts them to Reddit."""

import os
import requests
import praw

CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']

_KEY = os.environ['_KEY']

LOG_FILE = './processed_ids.txt'
CHANNEL_IDS_FILE = './channel_ids.txt'


def load_file(file):
    """Loads the log file and creates it if it doesn't exist.
     Parameters
    ----------
    file : str
        The file to read
    Returns
    -------
    list
        A list of urls.
    """

    try:
        with open(file, 'r', encoding='utf-8') as temp_file:
            return temp_file.read().splitlines()
    except Exception:
        with open(LOG_FILE, 'w', encoding='utf-8') as temp_file:
            return []


def update_file(file, data):
    """Updates the log file.
    Parameters
    ----------
    file : str
        The file to write down.
    data : str
        The data to log.
    """

    with open(file, 'a', encoding='utf-8') as temp_file:
        temp_file.write(data + '\n')


def get_channel_items(channel):
    """Gets videos from api.

    Returns
    -------
    list
        A list of videos elements.

    """

    api_url = \
        'https://www.googleapis.com/youtube/v3/search?channelId={}&part=snippet&maxResults=3&order=date&key={}'.format(channel,
            _KEY)
    try:
        with requests.get(api_url) as response:
            print('request OK')
            data = response.json()
            return data['items']
    except:
        print('Error during request')
        exit()


def init_bot():
    """Reads the RSS feed."""

    # We create the Reddit instance.

    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         username=USERNAME, password=PASSWORD,
                         user_agent='testscript by /u/larry3000bot')

    # Get channels list and logged ids

    logged_ids = load_file(LOG_FILE)
    channel_ids = load_file(CHANNEL_IDS_FILE)

    for channel_id in channel_ids:
        try:

            # Get Channel videos

            videos = get_channel_items(channel_id)
            for video in reversed(videos):
                if video['id']['videoId'] not in logged_ids:
                    video_url = 'https://www.youtube.com/watch?v=' \
                        + video['id']['videoId']
                    title = video['snippet']['title']

                    #to avoid garbage videos from this specific channel
                    if channel_id == "UC2sxxXRBL5SgY0fI58BrOCA" and "clip" in title.lower():
                        continue

                    print("posting {}".format(video_url))
                    reddit.subreddit('lazonacero').submit(title=title,
                            url=video_url, flair_id='3a671302-f61b-11ea-96e0-0ef730440ba1')
                    update_file(LOG_FILE, video['id']['videoId'])
        except Exception as e:
            print(e)
            continue

    print('end of script')


if __name__ == '__main__':

    init_bot()
