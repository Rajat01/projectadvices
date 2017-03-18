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
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if not request.user.is_anonymous:
                    serializer.save(asked_by=request.user)
                    serializer.save()
                    resp_dict.update(result=serializer.data, message='Success')
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    resp_dict.update(message='Not a valid user', error=1)
                    return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                print e
                resp_dict.update(message='Something went wrong', error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_question_list(request, format=None):
    """List all the questions"""
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'GET':
        try:
            question = Questions.objects.all()
            serializer = QuestionSerializer(question, many=True)
            resp_dict.update(result=serializer.data)
            return Response(resp_dict, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            resp_dict.update(message='Something went wrong', error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def update_question(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        if not request.user.is_anonymous:
            pass


@api_view(['DELETE'])
def delete_question(request, pk, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'DELETE':
        if not request.user.is_anonymous:
            question_to_delete = Questions.objects.get(pk=pk)
            if question_to_delete:
                advices_related_to_ques = Advices.objects.filter(question_id=pk)
                if request.user.id == question_to_delete.asked_by_id:
                    if advices_related_to_ques:
                        advices_related_to_ques.delete()
                    question_to_delete.delete()
                    resp_dict.update(message='Successfully deleted')
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    resp_dict.update(message='Sorry this question was not asked by you', error=1)
                    return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
            else:
                resp_dict.update(message='Questions does not exist')
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            resp_dict.update(message='Not a valid user', error=1)
            return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)

