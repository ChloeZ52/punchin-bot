# punchin-bot

Suppose we are hosting a Study Room as Voice Channels in the Discord server.

Punchin Bot helps record how much time a user spends in the Study Room, which is stored in Google Sheets.

Example:

*On 2020-11-12, user chloezzzzz joins the Study Room at 14:45 and leaves the Study Room at 15:53.*

Google Sheets screenshot:

![Google Sheets](https://github.com/ChloeZ52/punchin-bot/blob/main/images/Google%20Sheets%20Example.png)

## Features

### Record study time

When user joins or leaves the Study Room, timestamp will be inserted for that day in Google Sheets.

### Retrieve study time

Example:

`$get_my_study_record`

Output:

`14:45 ~ 15:53`
