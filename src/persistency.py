import os

from sheets_api import SheetsAPI
from youtube_api import YTVideo


class Persistency():
    def __init__(self, spreadsheet_id):
        self.sheets_api = SheetsAPI(spreadsheet_id)
        self.id_videos = [video.video_id for video in self.get_all_videos()]
        self.last_empty_row = len(self.id_videos) + 1

    def get_all_videos(self):
        filtered_content = [content for content in self.sheets_api.read_value_rows(
            'A', 2, 'L') if content is not None and content]
        return [YTVideo(video_data[0], video_data) for video_data in filtered_content]

    def save_video(self, video):
        """Save the youtube video inside the spreadsheet."""
        if video.video_id not in self.id_videos:
            self.sheets_api.write_row(
                'A', self.last_empty_row, *video.to_list())
            self.last_empty_row += 1
            self.id_videos.append(video.video_id)

    def batch_save_videos(self, videos):
        filtered_videos = [
            video for video in videos if video.video_id not in self.id_videos]
        if(len(filtered_videos) > 0):
            print("Sending {} videos to google sheets".format(len(filtered_videos)))
            list_content = [video.to_list() for video in filtered_videos]
            self.sheets_api.batch_write_rows(
                'A', self.last_empty_row, list_content)
            self.last_empty_row += len(filtered_videos)
            self.id_videos.append(
                [video.video_id for video in filtered_videos])

    def is_video_saved(self, video_id):
        return True if video_id in self.id_videos else False


if __name__ == '__main__':
    persistency = Persistency(os.environ.get('sheet_id'))
