'''
This is the module to comunicate with the aws cognito. we have make a class which we
 can use to perform CURD operation upon a user.
 As well as a user can login and get the jwt token to perform rest of the work of our website.
 For this module  *******user pool is configured for email alias.
'''

import boto3
from django.conf import settings

# Here we are getting all the values related to the module which is required for
# the user to configure in settings.py file with the same namming convention
# UserPoolId = settings.UserPoolId   #'us-east-1_rT2J0mF11'
# clientId =  settings.clientId                        #'127dneql84oj5mtlubcvc5hag8'
# aws_access_key_id = settings.AWS_ACCESS_KEY                            #'AKIAXLSZRNQVD4KPYHPP'
# aws_secret_access_key = settings.AWS_SECRET_KEY                    #'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'
# region_name = settings.REGION_NAME                      #'us-east-1'
UserPoolId = 'us-east-1_rT2J0mF11'
clientId = '127dneql84oj5mtlubcvc5hag8'
aws_access_key_id = 'AKIAXLSZRNQVD4KPYHPP'
aws_secret_access_key = '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'
region_name = 'us-east-1'


class AWSCognito:
    def __init__(self):
        self.client = boto3.client('cognito-idp', region_name=region_name,
                                   aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        self.UserPoolID = UserPoolId
        self.ClientId = clientId

    def AWS_Create_User(self, username, email, password):  # this Function will help us to create a new User.
        try:
            response = self.client.admin_create_user(
                UserPoolId=self.UserPoolID,
                Username=email,
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': email,
                    },
                ],
                ValidationData=[
                    {
                        'Name': 'name',
                        'Value': username
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
            return response
        except Exception as error:
            print('error is Create user -->', error)
            # logger.error("FAILED |  AWS_Create_User Inner fn!" + str(status.HTTP_400_BAD_REQUEST) + " "+str(error))
            return error

    def AWS_SignIn(self, email, password):  # this function is return a new jwt token
        try:
            response = self.client.admin_initiate_auth(
                UserPoolId=UserPoolId,
                ClientId=clientId,
                AuthFlow='ADMIN_NO_SRP_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                },
            )
            # logger.info("SUCCESS |  AWS_SignIn Inner fn!" + str(status.HTTP_200_OK) + " "+str(response))
            return response, True
        except Exception as error:
            print(error, '<aws cognito signIn')
            error_value = str(error)
            # logger.error("FAILED |  AWS_SignIn Inner fn!" + str(status.HTTP_400_BAD_REQUEST) + " "+str(error))
            return error_value

    def AWS_first_login(self, username, password,
                        session_id):  # this function will return the jwt token from the session id
        try:
            print(username, '<<<<<<<<<<<<<username>>>>>>>>>>>>>>')
            print(password, '<<<<<<<<<<<<<password>>>>>>>>>>>>>>')
            print(session_id, '<<<<<<<<<<<<<session_id>>>>>>>>>>>>>>')
            response = self.client.admin_respond_to_auth_challenge(
                UserPoolId=UserPoolId,
                ClientId=clientId,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ChallengeResponses={
                    'USERNAME': username,
                    'NEW_PASSWORD': password,
                    'name': ""
                },
                Session=session_id,
            )
            print(response)
            return response
        except Exception as err:
            print(err)

    def AWS_Change_Password(self, accesstoken, previouspassword, proposedpassword):
        try:
            response = self.client.change_password(
                PreviousPassword=previouspassword,
                ProposedPassword=proposedpassword,
                AccessToken=accesstoken
            )
            return response
        except Exception as error:
            return error

    def Refresh_Token(self, Token):
        try:
            response = self.client.admin_initiate_auth(
                UserPoolId=self.UserPoolID,
                ClientId=self.ClientId,
                AuthFlow='REFRESH_TOKEN',
                AuthParameters={
                    'REFRESH_TOKEN': Token
                },
            )
            return response
        except Exception as error:
            return error

    def Aws_get_user(self, Token):
        try:
            response = self.client.get_user(
                AccessToken=Token
            )
            return response
        except Exception as error:
            print(error, "<<<<<<Aws_get_user")
            return error

    def AWS_forgotpassword(self, email, password):
        try:
            response = self.client.admin_set_user_password(
                UserPoolId=self.UserPoolID,
                Username=email,
                Password=password,
                Permanent=True
            )
            return response
        except Exception as error:
            return error

    def AWS_DeleteUser(self, email):
        try:
            response = self.client.admin_delete_user(
                UserPoolId=self.UserPoolID,
                Username=email
            )
            return response
        except Exception as error:
            return error

    def AWS_Check_User(self, email):
        try:
            response = self.client.admin_get_user(
                UserPoolId=self.UserPoolID,
                Username=email
            )
            # print(response,'Getting value from aws!')
            return response
        except Exception as error:
            return error

# send = AWSCognito().AWS_Create_User
# response = send('nipur1','nipur2@yopmail.com', 'Qwerty@2')
# print(response,"<<<<Hi we are geting the response of the awscognito?")
login = AWSCognito().AWS_SignIn
resp = login('nipur1', 'Qwerty@1')
print(resp)
AccessToken = resp[0]['AuthenticationResult']['AccessToken']
# print(session_id)
# first_login = AWSCognito()
# print(first_login.AWS_first_login(username='nipur1@yopmail.com', password='Qwerty@2', session_id=session_id))


previouspassword = 'Qwerty@2'
newpassword = 'Qwerty@1'
change_password = AWSCognito().AWS_Change_Password(AccessToken,previouspassword,newpassword)
print(change_password,"<<<<<<<<<<<<<<<<<Here we are geting the response of the changepassword")

# s = resp
#
# # print
# print(resp)
# auth= s['AuthenticationResult']['AccessToken']
# refresh = s['AuthenticationResult']['RefreshToken']
# idtoken = s['AuthenticationResult']['IdToken']
# print(auth, refresh, idtoken)


# https://djangostars.com/blog/bootstrap-django-app-with-cognito/
