from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Questions, Advices
from serializers import QuestionSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.test import force_authenticate


@csrf_exempt
@api_view(['POST'])
def create_question(request, format=None):
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(asked_by=request.user)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_question_list(request, format=None):
    """List all the questions"""
    if request.method == 'GET':
        question = Questions.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)


@api_view(['DELETE'])
def delete_question(request, pk, format=None):
    resp_dict = {}
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
                return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
        except:
            resp_dict['msg'] = 'Questions does not exist'
            return Response(resp_dict)


# @api_view(['GET', 'POST'])
# def advices_info(request, format=None):
#     pass
