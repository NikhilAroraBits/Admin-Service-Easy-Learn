import boto3
from secrets import access_key, secret_access_key
import os
import easygui


clinet = boto3.client('s3',
                  aws_access_key_id=access_key,
                  aws_secret_access_key=secret_access_key)

for file in os.listdir():
    if '.py' in file:
        easygui.msgbox(str(access_key), title="simple gui")
        upload_file_bucket = 'microsoftcoursevedio'
        upload_file_key = 'python/' + str(file)
        clinet.upload_file(file,upload_file_bucket,upload_file_key)