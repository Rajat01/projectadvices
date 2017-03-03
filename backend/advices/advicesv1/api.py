from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token





@api_view(['POST'])
def sign_up(request):
    resp_dict = {}
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email')
    password = request.data.get('password')
    username = request.data.get('username')
    user_created = User.objects.create_user(username, email, password)
    token = Token.objects.get(user=user_created)
    user = authenticate(username=username, password=password)
    login(request, user)
    resp_dict['access_token'] = token.key
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
        #response_dict['session_key'] = request.user.username
        resp_dict['access_token'] = request.auth
        resp_dict['status_msg'] = 'Login Successful'
        return Response(resp_dict)
    return Response(status=status.HTTP_304_NOT_MODIFIED)




@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)












