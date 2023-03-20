from __future__ import print_function

import google.auth,os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from creds import token

def GetListWrithID(N):
    creds = token()
    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)
    
        resource = service.files()
        result = resource.list(pageSize=N, fields="files(id, name)").execute()
    
        # return the result dictionary containing 
        # the information about the files
        #return result
    
    except HttpError as error:
        print(F'An error occurred: {error}')
        result = None

    return result




result_dict = GetListWrithID(5)
  
  
  
# Extract the list from the dictionary
file_list = result_dict.get('files')
  
  
# Print every file's name
for file in file_list:
    print(file['name'],file['id'])