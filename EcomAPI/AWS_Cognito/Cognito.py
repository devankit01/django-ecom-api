import boto3
from django.conf import settings

aws_access_key_id = 'AKIAXLSZRNQVD4KPYHPP'
aws_secret_access_key = '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'
client = boto3.client()
print(client)
UserPoolId = 'us-east-1_Ym1mvMTfV'
clientId= '1429dih4qdm2vdkekq481sk8m1'

class AWSCognito:
    def __init__(self):
        self.client == boto3.client('cognito-idp', region_name=settings.REGION_NAME,
                      aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
    def AWS_Create_User(self,email, password):
        try:
            print(email, '<aws email for Create User')
            print(password, '<aws password for Create User')
            response = self.client.admin_create_user(
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
            print(response)
            # logger.info("SUCCESS |  AWS_Create_User Inner fn!" + str(status.HTTP_200_OK) + " "+str(response))
            return 'true'
        except Exception as error:
            print('error is Create user -->', error)
            # logger.error("FAILED |  AWS_Create_User Inner fn!" + str(status.HTTP_400_BAD_REQUEST) + " "+str(error))
            return error
            
    def AWS_SignIn(email,password):
        try:
            response = client.admin_initiate_auth(
                UserPoolId=UserPoolId,
                ClientId=clientId,
                AuthFlow= 'ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                },
            )
            # logger.info("SUCCESS |  AWS_SignIn Inner fn!" + str(status.HTTP_200_OK) + " "+str(response))
            return response,True
        except Exception as error:
            print(error,'<aws cognito signIn')
            error_value = str(error)
            # logger.error("FAILED |  AWS_SignIn Inner fn!" + str(status.HTTP_400_BAD_REQUEST) + " "+str(error))
            return False,error_value

    def AWS_first_login(self,username,password,session_id):
            try:

                print(username,'<<<<<<<<<<<<<username>>>>>>>>>>>>>>')
                print(password,'<<<<<<<<<<<<<password>>>>>>>>>>>>>>')
                print(session_id,'<<<<<<<<<<<<<session_id>>>>>>>>>>>>>>')
                response = client.admin_respond_to_auth_challenge(
                    UserPoolId=UserPoolId,
                    ClientId=clientId,
                    ChallengeName='NEW_PASSWORD_REQUIRED',
                    ChallengeResponses={
                        'USERNAME': username,
                        'NEW_PASSWORD': password
                    },
                    Session=session_id,
                )
                print(response)
                return response
            except Exception as err:
                print(err)



# response = client.admin_create_user(
#             UserPoolId=UserPoolId,
#             Username='nipur1@yopmail.com',
#             UserAttributes=[
#                 {
#                     'Name': 'email',
#                     'Value': 'nipur1@yopmail.com',
#                 },
#             ],
#             # ValidationData=[
#             #     {
#             #         'Value': ''
#             #     },
#             # ],
#             #         'Name': '',
#
#             TemporaryPassword='Qwerty@2',
#             ForceAliasCreation=False,
#             MessageAction='SUPPRESS',
#             DesiredDeliveryMediums=[
#                 'EMAIL',
#             ],
#             ClientMetadata={
#                 # 'string': 'string'
#             }
#         )
# print(response)
# send = AWSCognito.AWS_Create_User
# send('nipur@yopmail.com', 'Qwerty@2')
login = AWSCognito.AWS_SignIn
resp = login('nipur1@yopmail.com', 'Qwerty@2')
session_id = resp[0]['Session']
print(session_id)
first_login = AWSCognito()
print(first_login.AWS_first_login(username='nipur1@yopmail.com', password='Qwerty@2',session_id=session_id))



# s = resp
#
# # print
# print(resp)
# auth= s['AuthenticationResult']['AccessToken']
# refresh = s['AuthenticationResult']['RefreshToken']
# idtoken = s['AuthenticationResult']['IdToken']
# print(auth, refresh, idtoken)


# https://djangostars.com/blog/bootstrap-django-app-with-cognito/