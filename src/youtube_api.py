import json
import os

import requests

from youtube_scraper import Scrapper

""" get youtube api from environment variable """
youtube_api_key = os.environ['youtube_api_key']


class YTVideo():
    def __init__(self, video_id, complete_video_data=None):
        self.video_id = video_id
        if complete_video_data is None:
            try:
                self.__load_video_from_list_values(
                    Scrapper(video_id).to_list())
            except Exception:
                print('Loading video {} from youtube api'.format(video_id))
                self.__load_video_from_youtube(video_id)
        elif isinstance(complete_video_data, list):
            self.__load_video_from_list_values(complete_video_data)

    def __load_video_from_youtube(self, video_id):
        """ load all the data for the video from youtube"""
        # self.channel_id = channel_id
        snippet = self.__get_stats_video(self.video_id)
        self.channel_id = snippet['channelId']
        self.title = snippet['title']
        self.publish_date = snippet['publishedAt']
        self.description = snippet['description']
        self.thumbnail = snippet['thumbnails']['medium']['url']
        self.category = snippet['categoryId']
        self.tags = snippet['tags'] if 'tags' in snippet else []

        if 'defaultAudioLanguage' in snippet:
            self.language = snippet['defaultAudioLanguage']
        elif 'defaultAudioLanguage' in snippet:
            self.language = snippet['defaultLanguage']
        else:
            self.language = 'ND'

    def __load_video_from_list_values(self, video_data):
        """ Load the video from a list of values"""
        self.title = video_data[1]
        self.views = video_data[2]
        self.likes = video_data[3]
        self.dislikes = video_data[4]
        self.comments = video_data[5]
        self.thumbnail = video_data[6]
        self.publish_date = video_data[7]
        self.category = video_data[8]
        self.language = video_data[9]
        self.channel_id = video_data[10]
        self.tags = video_data[11].split(";") if len(video_data) >= 12 else []

    def to_list(self):
        """ Transform the video in a list of values"""
        tags = ';'.join(self.tags)
        return [self.video_id, self.title, self.views, self.likes, self.dislikes, self.comments, self.thumbnail, self.publish_date, self.category, self.language, self.channel_id, tags]

    def __get_stats_video(self, video_id):
        """ get the statistics for a given video videos from youtube"""
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/videos?key={}&part=statistics&part=snippet&part=id&id={}'.format(youtube_api_key, video_id))
        check_youtube_quota(response)
        video = response.json()['items'][0]
        stats = video['statistics']

        self.views = stats['viewCount']
        self.likes = stats['likeCount'] if 'likeCount' in stats else 0
        self.dislikes = stats['dislikeCount'] if 'dislikeCount' in stats else 0
        self.comments = stats['commentCount'] if 'commentCount' in stats else 0

        if 'snippet' not in video:
            raise Exception('Youtube API Quota exceeded')
        return video['snippet']

    def __str__(self):
        return '#' + self.title + ' - views: ' + str(self.views) + ' - likes: ' + str(self.likes) + ' - dislikes: ' + str(self.dislikes) + ' - date:' + self.publish_date


def get_all_youtube_videos(channel_id):
    """ get the all videos ( with complete data ) from a youtube channel """
    id_videos = get_list_id_videos(channel_id)
    return [YTVideo(video_id) for video_id in id_videos]


def get_youtube_videos_from_list(list_ids):
    """ get the videos ( with complete data ) from the list of video ids informed """
    print('constructing youtube video from id')
    return [YTVideo(video_id) for video_id in list_ids]


def get_list_id_videos(channel_id):
    """ get the ids for all videos from a youtube channel """
    response = requests.get(
        'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&key={}&maxResults=50&playlistId={}'
        .format(youtube_api_key, __get_id_upload_playlist(channel_id)))
    check_youtube_quota(response)

    video_data = response.json()

    videos = response.json()['items']
    print('Getting {} videos from channel {}'.format(
        len(videos), channel_id))

    while 'nextPageToken' in video_data:
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&key={}&maxResults=50&playlistId={}&pageToken={}'
            .format(youtube_api_key, __get_id_upload_playlist(channel_id), video_data['nextPageToken']))
        check_youtube_quota(response)
        video_data = response.json()
        videos.extend(video_data['items'])
        print('Getting more {} videos from channel {}'.format(
            len(video_data['items']), channel_id))
    return [video['contentDetails']['videoId'] for video in videos]


def get_youtube_video(video_id):
    """ get the complete data for the youtube video with the informed video id """
    try:
        return YTVideo(video_id)
    except Exception:
        print('(500)Error creating the video ' + video_id)
        return None


def scrape_youtube_video(video_id):
    pass


def __get_id_upload_playlist(channel_id):
    """ get the id from the playlist containing all videos of a channel """
    response = requests.get(
        'https://www.googleapis.com/youtube/v3/channels?key={}&part=contentDetails&id={}'.format(youtube_api_key, channel_id))
    check_youtube_quota(response)
    return response.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def check_youtube_quota(response):
    if response.status_code == 403:
        raise Exception('Youtube API Quota exceeded')
