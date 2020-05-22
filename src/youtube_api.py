import json
import os

import requests

""" get youtube api from environment variable """
youtube_api_key = os.environ['youtube_api_key']

channel_videos_amount = 200


class YTVideo():
    def __init__(self, video_id, channel_id=None):
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
        """ get the statistics for a given video videos from youtube"""
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
    """ get the latest 200 videos from a youtube channel """
    response = requests.get(
        'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&key={}&maxResults={}&playlistId={}'.format(youtube_api_key, channel_videos_amount, __get_id_upload_playlist(channel_id)))
    videos = response.json()
    return [YTVideo(video['contentDetails']['videoId'], channel_id) for video in videos['items']]


def get_youtube_video(video_id):
    return YTVideo(video_id)


def __get_id_upload_playlist(channel_id):
    """ get the id from the playlist containing all videos of a channel """
    response = requests.get(
        'https://www.googleapis.com/youtube/v3/channels?key={}&part=contentDetails&id={}'.format(youtube_api_key, channel_id))
    return response.json()['items']['contentDetails']['uploads']
