import json
import os
import sys

from youtube_api import get_youtube_videos


def main():
    verify_variables()
    videos = get_videos_web("../channels.txt")
    print('{} videos were scrapped from the web'.format(len(videos)))


def get_videos_web(channels_file_name):
    videos = []
    with open('../output_video_log.txt', 'a') as output:
        log(output, 'Begining to parse youtube videos\n')
        """Get a list of objects representing youtube videos."""

        channels_id = get_channels_id(channels_file_name)
        for channel_id in channels_id:

            channel_videos = []  # get_youtube_videos(channel_id)
            # videos.extend(channel_videos)

            log(output, '[{}] a total of {} videos were processed for the channel.\n'.format(
                channel_id, len(channel_videos)))
        log(output, 'Complete, {} youtube channels were parsed resulting in {} videos\n'.format(
            len(channels_id), len(videos)))
    return videos


def log(output, message):
    print(message)
    output.write(message)


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
