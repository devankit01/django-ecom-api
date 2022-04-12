from rest_framework import status

def out_of_process_response():
    response = {
        'status': 'out_of_process',
        'code': status.HTTP_400_BAD_REQUEST,
        'message_en': "You can't log in anymore!",
        'message_nl': "Je kunt helaas niet (meer) inloggen!",
        'data': []
    }
    return response
def User_unauthorized_db():
    response = {
        'data': [],
        'status': 'error',
        'code': status.HTTP_400_BAD_REQUEST,
        'message_en': 'You are not a Authorize Person!',
        'message_nl': 'U bent geen gemachtigde!',
    }
    return response
def User_unauthorized_aws():
    response = {
        'status': 'UnAuthorized',
        'code': status.HTTP_401_UNAUTHORIZED,
        'message_en': 'UnAuthrorize access token!',
        'message_nl': 'Autorisatie van toegangstoken ongedaan maken!',
        'data': []
    }
    return response

def Success_response(data=[]):
    response = {
        'status': 'success',
        'code': status.HTTP_200_OK,
        'message_en': '',
        'message_nl': '',
        'data': data
    }
    return response

def Failure_response(data=[]):
    response = {
        'status': 'Failure',
        'code': status.HTTP_400_BAD_REQUEST,
        'message_en': '',
        'message_nl': '',
        'data': data
    }
    return response

def Error_response(data=[]):
    response = {
        'status': 'error',
        'code': status.HTTP_400_BAD_REQUEST,
        'message_en': '',
        'message_nl': '',
        'data': data
    }
    return response

def Internal_servevr_error(data=[]):
    response = {
        'status' : 'Internal Server Error',
        'code' : status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message_en' : '',
        'message_nl' : '',
        'data' : data
    }
    return response

