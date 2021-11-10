from googleapiclient.discovery import build
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def create_gsheet_client():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = service_account.Credentials.from_service_account_file(
        '../google/google_credential.json', scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    return service.spreadsheets()
