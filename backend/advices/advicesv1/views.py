from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Questions, Advices
from serializers import QuestionSerializer, AdviceSerializer
from django.db.models import F
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
@api_view(['POST'])
def create_question(request, format=None):
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            serializer.save(asked_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_question_list(request, format=None):
    """List all the questions"""
    if request.method == 'GET':
        question = Questions.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def update_question_upvote_count(request, format=None):
    if request.method == 'POST':
        request_data = request.data
        question_id = request_data.get('id')
        question_obj = Questions.objects.filter(pk=question_id)
        question_obj.update(up_votes=F('up_votes') + 1)
        serializer = QuestionSerializer(question_obj, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
def delete_question(request, pk, format=None):
    resp_dict = {}
    resp_dict['msg'] = 'Question does not exist'
    if request.method == 'DELETE':
        advices_related_to_ques = Advices.objects.filter(question_id=pk)
        if advices_related_to_ques:
            advices_related_to_ques.delete()
        try:
            question_to_delete = Questions.objects.get(pk=pk)
            if request.user.id == question_to_delete.asked_by_id:
                question_to_delete.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                resp_dict['error'] = 1
                resp_dict['err_msg'] = 'Sorry this question was not asked by you'
                return Response(resp_dict)
        except:
            return Response(resp_dict)


@api_view(['POST'])
def create_advice(request, format=None):
    if request.method == 'POST':
        request_data = request.data
        print request_data
        serializer = AdviceSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            serializer.save(advised_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_advices(request, pk, format=None):
    if request.method == 'GET':
        advices = Advices.objects.filter(question_id=pk)
        serializer = AdviceSerializer(advices, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def update_advice_upvote_count(request, pk, format=None):
    if request.method == 'POST':
        request_data = request.data
        advice_id = request_data.get('id')
        advice_obj = Advices.objects.filter(pk=advice_id)
        advice_obj.update(up_votes=F('up_votes') + 1)
        serializer = AdviceSerializer(advice_obj, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
def delete_advice_question(request, pk):
    resp_dict = {}
    if request.method == 'DELETE':
        advice_to_delete = Advices.objects.get(pk=pk)
        print 'request.user.id: {0}, advised_by: {1}'.format(request.user.id, advice_to_delete.advised_by_id)
        if request.user.id == advice_to_delete.advised_by_id:
            advice_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            resp_dict['error'] = 1
            resp_dict['err_msg'] = 'Sorry, this advice was not given by you'
            return Response(resp_dict)


@api_view(['GET', 'POST'])
def advices_info(request, format=None):
    pass

