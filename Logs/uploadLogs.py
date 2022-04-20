import os
from django.conf import settings
from datetime import datetime, timedelta
from os import listdir
from modules import s3_bucket
def logUpload():
    directory_path = os.getcwd()
    folder_name = '/Logs/'
    folder_dir_path = directory_path + folder_name
    lastDay = datetime.today() - timedelta(days=1)
    files_path = [folder_dir_path+x for x in listdir(folder_dir_path) if x.endswith(str(lastDay)[:10]) ]
    #Creating S3 Resource From the Session.
    for source_file in files_path:
        file_name = source_file.split(folder_name)[1]
        uploadingFile = s3_bucket.uploadFileToS3(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY,settings.BUCKET_NAME,source_file,'Log',file_name)
        print(uploadingFile)
