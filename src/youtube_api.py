import json
import os

import requests

""" get youtube api from environment variable """
youtube_api_key = os.environ['youtube_api_key']


class YTVideo():
    def __init__(self, video_id, channel_id):
        self.video_id = video_id
        self.channel_id = channel_id
        snippet = self.__get_stats_video(video_id)

        self.title = snippet['title']
        self.publish_date = snippet['publishedAt']
        self.description = snippet['description']
        self.thumbnail = snippet['thumbnails']['medium']
        self.category = snippet['categoryId']
        self.audio_language = snippet['defaultAudioLanguage']
        self.tags = snippet['tags'] if 'tags' in snippet else []

    def __get_stats_video(self, video_id):
        """ get the latest 50 videos from a youtube channel """
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/videos?key={}&part=statistics&part=snippet&part=id&id={}'.format(youtube_api_key, video_id))
        video = response.json()['items'][0]
        stats = video['statistics']

        self.views = stats['viewCount']
        self.likes = stats['likeCount']
        self.dislikes = stats['dislikeCount']
        self.comments = stats['commentCount']
        return video['snippet']

    def __str__(self):
        return '#' + self.title + ' - views: ' + str(self.views) + ' - likes: ' + str(self.likes) + ' - dislikes: ' + str(self.dislikes) + ' - date:' + self.publish_date


def get_youtube_videos(channel_id):
    """ get the latest 50 videos from a youtube channel """
    response = requests.get('http://www.mocky.io/v2/5ec63f403200005e00d74bcf')
    # 'https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&fields=,items(id(videoId))&part=id&maxResults=2'.format(youtube_api_key, channel_id))
    videos = response.json()
    return [YTVideo(video['id']['videoId'], channel_id) for video in videos['items']]
