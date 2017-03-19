from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from serializers import UserSerializer

'''This contains all auth related apis'''


@api_view(['POST'])
def sign_up(request):
    resp_dict = dict(message='', error=0, result='')
    try:
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')
        user_created = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        token = Token.objects.get(user=user_created)
        user = authenticate(username=username, password=password)
        login(request, user)
        resp_dict.update(result=dict(access_token=token.key, user_id=request.user.id), message='Sign-up successful')
        return Response(resp_dict, status=status.HTTP_201_CREATED)
    except Exception as e:
        resp_dict.update(message=str(e), error=1)
        return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    resp_dict = dict(message='', error=0, result='')
    try:
        #a = []
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token = Token.objects.get(user=user)
            # print "login_user api error {0}".format(request.auth)
            #a.append(dict(access_token=token.key, user_id=request.user.id))
            resp_dict.update(result=dict(access_token=token.key, user_id=request.user.id), message='Login successful')
            #resp_dict.update(result=a, message='Login successful')
            print resp_dict
            return Response(resp_dict, status=status.HTTP_200_OK)
        else:
            resp_dict.update(message='User not found', error=1)
            return Response(resp_dict, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        resp_dict.update(message=str(e), error=1)
        return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_id_user_mapping(request, format=None):
    user_info = User.objects.all()
    serializer = UserSerializer(user_info, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
