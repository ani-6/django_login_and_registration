from __future__ import print_function

import google.auth,os
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from .creds import token
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/drive']

def UploadToDrive(filename, folder_id,mimetyp):
    creds = token()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
        file_name = filename.split("/")[-1]

        file_metadata = {'name': file_name,'parents':[folder_id]}
        media = MediaFileUpload(filename,
                                mimetype=mimetyp)
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

def DeleteFile(file_id):
    creds = token()
  
    # Connect to the API service
    service = build('drive', 'v3', credentials=creds)
  
    # request a list of first N files or 
    # folders with name and id from the API.
    result = service.files().delete(fileId=file_id).execute()
    result = "deleted"
    # return the result dictionary containing 
    # the information about the files
    return result

def ListLabel():
    creds = token()

    service = build('drive', 'v3', credentials=creds)

    response=service.files().list(pageSize=1000).execute()
    files=response.get('files')
    nextPageToken=response.get('nextPageToken')

    while nextPageToken:
        response=service.files().list(pageSize=1000, pageToken=nextPageToken).execute()
        files.extend(response.get('files'))
        nextPageToken=response.get('nextPageToken')

    df = pd.DataFrame(files)
    df = df.sort_values(by=['mimeType'])
    return df

def CreateFolder(folderName, parentID = None):
    try:
        creds = token()
        service = build('drive', 'v3', credentials=creds)
        # Create a folder on Drive, returns the newely created folders ID
        body = {
          'name': folderName,
          'mimeType': "application/vnd.google-apps.folder"
        }
        if parentID:
            body['parents'] = [parentID]
        root_folder = service.files().create(body = body).execute()
        return root_folder['id']

    except HttpError as error:
        print(F'An error occurred: {error}')
        return None