import os
import boto3
from django.conf import settings
from datetime import datetime, timedelta
from os import listdir
def logUpload():
    directory_path = os.getcwd()
    folder_name = '/Logs/'
    folder_dir_path = directory_path + folder_name
    lastDay = datetime.today() - timedelta(days=1)
    files_path = [folder_dir_path+x for x in listdir(folder_dir_path) if x.endswith(str(lastDay)[:10]) ]

    #Creating Session With Boto3.

    session = boto3.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

    #Creating S3 Resource From the Session.
    for i in files_path:
        s3 = session.resource('s3')
        file_name = i.split(folder_name)[1]
        object = s3.Object(settings.BUCKET_NAME, "Logs/"+file_name)
        result = object.put(Body=open(i, 'rb'))
