import boto3

def uploadFileToS3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,BUCKET_NAME,SOURCE_FILE,DESTINATION_DIR,FILE_NAME):
    session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    s3 = session.resource('s3')
    object = s3.Object(BUCKET_NAME, DESTINATION_DIR+"/"+FILE_NAME)
    result = object.put(Body=open(SOURCE_FILE, 'rb'))
    return result