from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from models import Questions, Advices
from serializers import QuestionSerializer, AdviceSerializer
from django.db.models import Count





@api_view(['POST'])
def create_question(request, format=None):

    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_question_list(request, format=None):

    """List all the questions"""
    if request.method == 'GET':
        question = Questions.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)



@api_view(['GET'])
def get_all_advices(request, pk, format=None):

    if request.method == 'GET':
        advices = Advices.objects.filter(question_id=pk)
        serializer = AdviceSerializer(advices, many=True)
        return Response(serializer.data)



@api_view(['POST'])
def create_advice(request, format=None):

    if request.method == 'POST':
        request_data = request.data
        print request_data
        serializer = AdviceSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def advices_info(request, format=None):
    pass



@api_view(['POST'])
def update_question_upvote_count(request, pk, format=None):

    if request.method == 'POST':
        upvote_count = Questions




# Create your views here.
