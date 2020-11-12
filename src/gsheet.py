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
        self.sheet = self.service.spreadsheets()

    def get_value(self, sheet_id, sheet_range):
        result = (
            self.sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
        )
        values = result.get("values", [])
        return values

    def get_user_index(self, sheet_id, user):
        user_arr = self.get_value(sheet_id, "Work Sheet!A:A")
        return user_arr.index([user]) + 1

    def get_today_index(self, sheet_id):
        index = self.get_value(sheet_id, "Lookup Sheet!A1")[0][0]
        lookup_formula = f'=SUBSTITUTE(ADDRESS(1,{index},4),"1","")'
        response = self.add_value(
            sheet_id,
            "Lookup Sheet!A2:A2",
            {"values": [[lookup_formula]]},
        )
        updatedData = response.get("updatedData")
        values = updatedData.get("values")
        return values[0][0] if len(values) != 0 else None

    def add_value(self, sheet_id, sheet_range, range_body):
        VALUE_INPUT_OPTION = "USER_ENTERED"
        request = self.sheet.values().update(
            spreadsheetId=sheet_id,
            range=sheet_range,
            valueInputOption=VALUE_INPUT_OPTION,
            body=range_body,
            includeValuesInResponse="true",
            fields="updatedData",
        )
        reseponse = request.execute()
        return reseponse