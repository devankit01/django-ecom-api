import os
import boto3
from django.conf import settings
from datetime import datetime, timedelta
from os import listdir
directory_path = os.getcwd()
folder = directory_path + '/Logs/'
print(folder)
lastDay = datetime.today() - timedelta(days=1)
files_path = [folder+x for x in listdir(folder) if x.endswith(str(lastDay)[:10]) ]
print(files_path)




#Creating Session With Boto3.

s3_client = boto3.client(service_name='s3', region_name='us-east-1',
                         aws_access_key_id='AKIAXLSZRNQVNIHKAEFH',
                         aws_secret_access_key='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')
#Creating S3 Resource From the Session.
# s3 = s3_client.resource('s3')
print(type(files_path))
for i in files_path:
    print(i, type(i))
    response = s3_client.upload_file(i, 'serverless-django3', 'AKIAXLSZRNQVNIHKAEFH')
    print(response)
