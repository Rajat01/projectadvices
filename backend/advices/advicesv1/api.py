from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes

'''This contains all auth related apis'''



@api_view(['POST'])
def sign_up(request):
    resp_dict = {}
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email')
    password = request.data.get('password')
    username = request.data.get('username')
    print "pehele: {0}".format(request.user)
    user_created = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    token = Token.objects.get(user=user_created)
    user = authenticate(username=username, password=password)
    login(request, user)
    resp_dict['access_token'] = token.key
    resp_dict['user_id'] = request.user.id
    resp_dict['status_msg'] = 'Sign-up Successful'
    return Response(resp_dict, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def login_user(request):
    resp_dict = {}
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        token = Token.objects.get(user=user)
        #print "login_user api error {0}".format(request.auth)
        resp_dict['access_token'] = token.key
        resp_dict['user_id'] = request.user.id
        resp_dict['status_msg'] = 'Login Successful'
        return Response(resp_dict)
    else:
        resp_dict['error'] = 1
        resp_dict['error_message'] = 'User does not exist'
        return Response(resp_dict)




@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)












