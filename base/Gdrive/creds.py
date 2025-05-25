import os
from pathlib import Path
from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/drive']


def token():
    creds = None
    # Define the SCOPES variable according to your requirements
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Convert BASE_DIR to a Path object
    base_dir = Path(settings.BASE_DIR)

    # Construct the file paths using the / operator
    token_path = base_dir / 'base' / 'Gdrive' / 'token.json'
    credentials_path = base_dir / 'base' / 'Gdrive' / 'credentials.json'

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token_file:
            token_file.write(creds.to_json())
    
    return creds