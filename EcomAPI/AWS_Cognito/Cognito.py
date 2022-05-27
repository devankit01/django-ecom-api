import boto3
from decouple import config

aws_access_key_id = config('AWS_ACCESS_KEY_ID_COGNITO')
aws_secret_access_key = config('AWS_SECRET_ACCESS_KEY_COGNITO')
client = boto3.client('cognito-idp', region_name=config('REGION_NAME'),
                      aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
UserPoolId =config('USER_POOL_ID')
clientId= config('CLIENT_ID')

class AWSCognito: 
    # this function is used to create user on aws cognito
    def AWS_Create_User(email, password): # this function takes two argument email and password
        try:
            response = client.admin_create_user(
                UserPoolId=UserPoolId, 
                Username=email,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email,
                    },
                ],
                TemporaryPassword=password,
                ForceAliasCreation=False,
                # MessageAction='SUPPRESS',
                DesiredDeliveryMediums=[
                    'EMAIL',
                ],
                ClientMetadata={
                    # 'string': 'string'
                }
            )
            return 'true'
        except Exception as error:
            return error
    # this function is used for signin through aws cognito 
    def AWS_SignIn(email,password):
        try:
            #admin_initiate_auth allow to authenticate
            response = client.admin_initiate_auth(
                UserPoolId=UserPoolId,
                ClientId=clientId,
                AuthFlow= 'ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                },
            )
            return response,True
        except Exception as error:
            error_value = str(error)
            return False,error_value


login = AWSCognito.AWS_SignIn
resp = login('userAWS1@yopmail.com', 'Ankit3@98')
s = resp 
auth= s['AuthenticationResult']['AccessToken']
refresh = s['AuthenticationResult']['RefreshToken']
idtoken = s['AuthenticationResult']['IdToken']



# https://djangostars.com/blog/bootstrap-django-app-with-cognito/