# This Service is us to send messages and at the same time delteing the messages and if you can to know about the messages
# You can simply use the method call recieve

'''......................................... Requirement of the module ...............................................
 Set up these keys in settings.py file of the project
         AWS_ACCESS_KEY = "**************"
        AWS_SECRET_KEY = "***********"
        AWS_SQS_QUEUE_NAME = "***********"
        REGION_NAME = '************'

'''

from EcomAPI.av_packages.comman_response import *
from django.conf import settings

try:
    import boto3
    import os
    import sys
    import json
except Exception as e:
    response = Internal_servevr_error(e)
    print(response)



# AWS_ACCESS_KEY = settings.AWS_ACCESS_KEY
# AWS_SECRET_KEY = settings.AWS_SECRET_KEY
# AWS_SQS_QUEUE_NAME = settings.AWS_SQS_QUEUE_NAME
# REGION_NAME = settings.REGION_NAME
AWS_ACCESS_KEY = 'AKIAT2MREPZ25SSYAELO'
AWS_SECRET_KEY = '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'
AWS_SQS_QUEUE_NAME = 'firstsqs'
REGION_NAME = 'us-east-1'
# queue_url = 'http://127.0.0.1:8000/api/check_sqs/'
class SQSQueue(object):
    def __init__(self, queueName=None):
        self.resource = boto3.resource('sqs', region_name=REGION_NAME,
                                       aws_access_key_id=AWS_ACCESS_KEY,
                                       aws_secret_access_key=AWS_SECRET_KEY,
                                       # endpoint_url = 'http://127.0.0.1:8000/api/check_sqs/'
                                       )
        self.queue = self.resource.get_queue_by_name(QueueName=AWS_SQS_QUEUE_NAME)
        self.QueueName = queueName

    def send(self, Message={}):
        data = json.dumps(Message)
        response = self.queue.send_message(MessageBody=data)
        return response

    def receive(self):
        try:
            queue = self.resource.get_queue_by_name(QueueName=self.QueueName)
            response = ''
            for message in queue.receive_messages():
                data = message.body
                data = json.loads(data)
                message.delete()
                response = Success_response(data)
            # else:
            #     data = "There is no data to show you at this moment!"
            #     response = Success_response(data)
        except Exception as err:
            response =  Failure_response(err)
        return response


if __name__ == "__main__":
    q = SQSQueue(queueName=AWS_SQS_QUEUE_NAME)
    Message_val = {"name":"Nipur SQS is working properly "}
    response = q.send(Message=Message_val)
    print(response)
    # data = q.receive()
    # print(data)