import random
import uuid
# from django.core.mail import send_mail
import boto3
import os
from django.conf import settings

class AWS_SNS:
    def sendSms(context):
        # SNS Integration
        print('------------INSIDE_________AWS_SNS=====',settings.AWS_ACCESS_KEY_ID)
        # SMS_TO = "+919140562195"  # Make sure is set in E.164 format.
        AWS_ACCESS_KEY_ID       = settings.AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY   = settings.AWS_SECRET_ACCESS_KEY
        REGION_NAME             = settings.REGION_NAME
        SENDER_ID               = settings.SENDER_ID
        SMS_TO                  = context['SMS_TO']
        MESSAGE                 = context['MESSAGE']


        range_start = 10**(6-1)
        range_end = (10**6)-1
        OTP = random.randint(range_start, range_end)
        message = '{}: {}'.format(str(MESSAGE),str(OTP))
        SMS_MESSAGE = message      
        # Create an SNS client
        try:
            clientSNS = boto3.client(
                "sns",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=REGION_NAME
            )
                    # Send your sms message.
            response = clientSNS.publish(
                PhoneNumber=SMS_TO,
                Message=SMS_MESSAGE,
                MessageAttributes={
                    'string': {
                        'DataType': 'String',
                        'StringValue': 'String',
                    },
                    'AWS.SNS.SMS.SenderID': {
                        'DataType': 'String',
                        'StringValue': SENDER_ID
                    }
                }
            )
            print(response,'getting response-------------------')
            return response,OTP
        except Exception as error:
            return False,error