import os

from sheets_api import SheetsAPI
from youtube_api import YTVideo


class Persistency():
    def __init__(self, spreadsheet_id):
        self.sheets_api = SheetsAPI(spreadsheet_id)
        self.last_empty_row = self.__find_last_empty_row(1)

    def save_video(self, video):
        """Save the youtube video inside the spreadsheet."""
        self.sheets_api.set_row('A', self.last_empty_row, *video.to_list())
        self.last_empty_row += 1

    def __find_last_empty_row(self, index_row):
        """Find which row inside the spreadsheet is empty."""
        value = self.sheets_api.read_value_single_cell('A', index_row)
        if value is None:
            return index_row
        return self.__find_last_empty_row(index_row + 1)


if __name__ == '__main__':
    persistency = Persistency(os.environ.get('sheet_id'))
    print(persistency.last_empty_row)
