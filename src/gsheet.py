from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint


class gsheet:
    def __init__(self):
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("sheets", "v4", credentials=self.creds)

    def get(self, sheet_id, sheet_range):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
        values = result.get("values", [])
        if not values:
            print("No data found.")
        else:
            for row in values:
                for v in row:
                    print(v)

    def add(self, sheet_id, sheet_range, range_body):
        VALUE_INPUT_OPTION = "RAW"

        # Call the Sheets API
        sheet = self.service.spreadsheets()

        # Update values
        request = sheet.values().update(
            spreadsheetId=sheet_id,
            range=sheet_range,
            valueInputOption=VALUE_INPUT_OPTION,
            body=range_body,
        )
        reseponse = request.execute()
        print(reseponse)