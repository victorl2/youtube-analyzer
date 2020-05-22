import json
import os

from youtube_api import get_youtube_videos

spreadsheet_id = '1PrnugvoV5hTwHl4Oi6PC-AySKTjvVJc2OBRHuuYVdps'
youtube_channels = [
    'UC70YG2WHVxlOJRng4v-CIFQ',
    ''
]


def main():
    if 'youtube_api_key' not in os.environ:
        print('The environment variable "youtube_api_key" is not defined, the key is required to run the app')

    videos = get_videos_web(youtube_channels)
    print('{} videos were scrapped from the web'.format(len(videos)))


def get_videos_web(channels):
    videos = []
    for channel_id in youtube_channels:
        videos.extend(get_youtube_videos(channel_id))
    return videos


if __name__ == '__main__':
    main()
