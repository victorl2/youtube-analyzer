import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class SheetsAPI():
    def __init__(self, sheet_id):
        self.sheet_id = sheet_id
        self.credentials = self.__get_credentials()
        self.service = build('sheets', 'v4', credentials=self.credentials)

    def __send_request(self, body):
        """Send a request to the googlespreadsheet's title."""
        response = self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.sheet_id, body=body).execute()

    def __get_credentials(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        credentials = None

        if os.path.exists('../token.pickle'):
            with open('../token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '../credentials.json', ['https://www.googleapis.com/auth/spreadsheets'])
                credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('../token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    def __read_value(self, column_name, row_number, column_name_target=None):
        """Read the value present in a cell inside the spreadsheet."""
        range = self.__get_range(column_name, row_number) if column_name_target is None else self.__get_range(
            column_name, row_number) + ":" + self.__get_range(column_name_target, row_number)

        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.sheet_id, range=range).execute()

        if result.get('values') is None:
            return [] if column_name_target is not None else None

        return result.get('values')[0] if column_name_target is not None else result.get('values')[0][0]

    def __get_range(self, column_name, row_number):
        """Get the range of one or more cells inside the spreadsheet."""
        return column_name + str(row_number)

    def set_value(self, column_name, row_number, new_value):
        """Set the value for a given cell in the spreadsheet."""
        cell_position = self.__get_range(column_name, row_number)
        body = {
            'values': [new_value if isinstance(new_value, list) else [new_value]]
        }

        result = self.service.spreadsheets().values().update(
            range=cell_position, valueInputOption='RAW', spreadsheetId=self.sheet_id, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

    def set_row(self, column_name, row_number, *values):
        """Set a row of values starting in a given cell inside the spreadsheet."""
        self.set_value(column_name, row_number, [value for value in values])

    def read_value_single_cell(self, column_name, row_number):
        return self.__read_value(column_name, row_number)

    def read_value_row(self, column_name, row_number, target_column_name):
        return self.__read_value(column_name, row_number, target_column_name)

    def update_title(self,  new_title):
        """Change the spreadsheet's title."""
        __send_request({
            'requests': {
                'updateSpreadsheetProperties': {
                    'properties': {
                        'title': 'Um titulo de teste'
                    },
                    'fields': 'title'
                }
            }
        })


if __name__ == '__main__':
    api = SheetsAPI(os.environ.get('sheet_id'))
    print(api.read_value_row('A', 1, 'L'))
    print("API Called")
