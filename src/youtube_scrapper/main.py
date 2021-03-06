import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from persistency import Persistency
from youtube_api import get_list_id_videos, get_youtube_video


def main():
    verify_variables()
    process_videos("../../channels.txt")


def process_videos(channels_file_name):
    videos = []
    persistency = Persistency(os.environ.get('sheet_id'))
    channels_id = get_channels_id(channels_file_name)

    log('Begining to parse youtube videos\n')

    for channel_id in channels_id:
        videos.extend(save_videos_youtube_channel(channel_id, persistency))

    log('Complete!! {} youtube channels were parsed resulting in {} videos\n'.format(
        len(channels_id), len(videos)))


def save_videos_youtube_channel(channel_id, persistency, output=None):
    log("Reading videos from channel {}".format(channel_id))

    id_videos = [video_id for video_id in get_list_id_videos(
        channel_id) if not persistency.is_video_saved(video_id)]
    log('\n{} videos to be processed for the channel\n'.format(len(id_videos)))

    videos = []
    processed_videos = []

    while len(id_videos) > 0:
        ids_to_process = id_videos[:120]
        id_videos = id_videos[120:]

        start_time = time.time()
        with ProcessPoolExecutor(max_workers=6) as executor:
            videos = [v for v in executor.map(
                get_youtube_video, ids_to_process) if v is not None]

        execution_time = time.time() - start_time
        log('{} videos parsed in {} seconds'.format(
            len(videos), execution_time))

        start_time = time.time()
        persistency.batch_save_videos(videos)
        execution_time = time.time() - start_time
        log('{} seconds to save {} videos\n'.format(execution_time, len(videos)))

        processed_videos.extend(videos)
        videos.clear()

    log('[{}] a total of {} videos were processed for the channel.\n'.format(
        channel_id, len(processed_videos)))
    return processed_videos


def log(message):
    print(message)


def get_channels_id(channels_file_name):
    """Get a list of channels id."""
    channels = []
    try:
        channels_file = open(channels_file_name)
        channels = [line.strip() for line in channels_file.readlines()]
    except IOError:
        print("A file is containing the channels is required to be present in the the project, the app needs to know which channels to get the videos from.")
        sys.exit()
    finally:
        channels_file.close()
    return channels


def verify_variables():
    """Check if all the variables needed to run the app are defined"""
    if 'youtube_api_key' not in os.environ:
        print('The environment variable "youtube_api_key" is not defined, the key is required to run the app')
        sys.exit()
    if 'sheet_id' not in os.environ:
        print('The environment variable "sheet_id" is not defined, a spreadsheet is required to run the app')
        sys.exit()


if __name__ == '__main__':
    main()
