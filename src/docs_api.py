from __future__ import print_function

import os.path
import pickle

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# https://developers.google.com/sheets/api/quickstart/python


def insert_text():
     requests = [
         {
            'insertText': {
                'location': {
                    'index': 25,
                },
                'text': 'text1'
            }
        },
                 {
            'insertText': {
                'location': {
                    'index': 50,
                },
                'text': 'text2'
            }
        },
                 {
            'insertText': {
                'location': {
                    'index': 75,
                },
                'text': 'text3'
            }
        },
    ]

    result = service.documents().batchUpdate(
        documentId=DOCUMENT_ID, body={'requests': requests}).execute()
