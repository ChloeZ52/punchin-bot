from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
VALUE_INPUT_OPTION = "USER_ENTERED"
TODAY_LOOKUP_RANGE = "Lookup Sheet!A1"
USER_COLUMN_LOOKUP_RANGE = "Lookup Sheet!A2:A2"
USER_RANGE = "Work Sheet!1:1"


class gsheet:
    def __init__(self):

        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("/Users/chloezeng/Documents/side-projects/punchin-bot/src/token.pickle"):
            with open("/Users/chloezeng/Documents/side-projects/punchin-bot/src/token.pickle", "rb") as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "/Users/chloezeng/Documents/side-projects/punchin-bot/src/credentials.json", SCOPES
                )
                self.creds = flow.run_local_server()
            # Save the credentials for the next run
            with open("/Users/chloezeng/Documents/side-projects/punchin-bot/src/token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("sheets", "v4", credentials=self.creds)
        self.sheet = self.service.spreadsheets()

    def get_value(self, sheet_id, sheet_range):
        result = (
            self.sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
        )
        values = result.get("values", [])
        return values

    def get_today_index(self, sheet_id):
        index = self.get_value(sheet_id, TODAY_LOOKUP_RANGE)[0][0]
        return None if index == "#N/A" else index

    def get_user_index(self, sheet_id, user):
        user_arr = self.get_value(sheet_id, USER_RANGE)
        try:
            index = user_arr[0].index(user) + 1
        except ValueError:
            print(f"user {user} is not found")
            return None

        lookup_formula = f'=SUBSTITUTE(ADDRESS(1,{index},4),"1","")'
        response = self.insert_value(
            sheet_id,
            USER_COLUMN_LOOKUP_RANGE,
            {"values": [[lookup_formula]]},
        )
        updatedData = response.get("updatedData")
        values = updatedData.get("values")
        return values[0][0]

    def get_update_address(self, sheet_id, user):
        user_index = self.get_user_index(sheet_id, user)
        today_index = self.get_today_index(sheet_id)
        if user_index == None or today_index == None:
            return None
        address = self.get_user_index(sheet_id, user) + str(
            self.get_today_index(sheet_id)
        )
        return address

    def insert_value(self, sheet_id, sheet_range, range_body):
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

    def append_value(self, sheet_id, sheet_range, range_body):
        request = self.sheet.values().append(
            spreadsheetId=sheet_id,
            range=sheet_range,
            valueInputOption=VALUE_INPUT_OPTION,
            body=range_body,
            includeValuesInResponse="true",
        )
        reseponse = request.execute()
        return reseponse