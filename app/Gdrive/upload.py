from __future__ import print_function

import google.auth,os
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive']


def token():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('app/Gdrive/token.json'):
        creds = Credentials.from_authorized_user_file('app/Gdrive/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'app/Gdrive/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('app/Gdrive/token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def UploadToDrive(filename, folder_id):
    creds = token()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        file_name = filename.split("/")[-1]

        file_metadata = {'name': file_name,'parents':[folder_id]}
        media = MediaFileUpload(filename,
                                mimetype='image/jpg')
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        file = file.get("id")
        ShareFile(file)
        shared = 1
        shared = bool(shared)
        context = {'fileName':file_name,'FileID':file,'FolderID':folder_id, 'Shared':shared}

    except HttpError as error:
        print(F'An error occurred: {error}')
        context = {}

    return context

def ShareFile(real_file_id):
    creds = token()
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        ids = []
        file_id = real_file_id

        def callback(request_id, response, exception):
            if exception:
                # Handle error
                print(exception)
            else:
                print(f'Request_Id: {request_id}')
                print(F'Permission Id: {response.get("id")}')
                ids.append(response.get('id'))

        # pylint: disable=maybe-no-member
        batch = service.new_batch_http_request(callback=callback)
        user_permission = {
            'type': 'anyone',
            'role': 'reader',
        }
        batch.add(service.permissions().create(fileId=file_id,
                                               body=user_permission,
                                               fields='id',))
    
        batch.execute()

    except HttpError as error:
        print(F'An error occurred: {error}')
        ids = None

    return ids

