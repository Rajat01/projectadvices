from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Questions, Advices
from serializers import QuestionSerializer, QuestionVoteSerializer, UserInfoQuestionSerializer
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


# """Create a question"""
@csrf_exempt
@api_view(['POST'])
def create_question(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.is_anonymous:
                serializer.save(asked_by=request.user)
                serializer.save()
                resp_dict.update(result=serializer.data, message='Success')
                return Response(resp_dict, status=status.HTTP_201_CREATED)
            else:
                resp_dict.update(message='Not a valid user', error=1)
                return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##################################################################################################

# """List all the questions"""
@api_view(['GET'])
def get_question_list(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'GET':
        try:
            question = Questions.objects.all()
            serializer = UserInfoQuestionSerializer(question, many=True)
            resp_dict.update(result=serializer.data)
            return Response(resp_dict, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            resp_dict.update(message=str(e), error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)

####################################################################################################

# """Update an existing question"""
@api_view(['POST'])
def update_question(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        if not request.user.is_anonymous:
            try:
                request_data = request.data
                question_id = request_data.get('question_id', None)
                question_to_update = Questions.objects.get(pk=question_id)
                serializer = QuestionVoteSerializer(question_to_update)
                if request.user.id == question_to_update.asked_by_id:
                    question_to_update.question = request_data.get('question')
                    question_to_update.save(update_fields=['question'])
                    resp_dict.update(result=serializer.data, message='Successfully updated question')
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    resp_dict.update(message='Sorry this question was not asked by you', error=1)
                    return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
            except ObjectDoesNotExist:
                resp_dict.update(message='Question object not found. Did you provide a valid question_id/question?',
                                 error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            resp_dict.update(message='Not a valid user', error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)

########################################################################################################


# """Delete a question with user check"""
@api_view(['DELETE'])
def delete_question(request, pk, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'DELETE':
        if not request.user.is_anonymous:
            try:
                question_to_delete = Questions.objects.get(pk=pk)
                advices_related_to_ques = Advices.objects.filter(question_id=pk)
                if request.user.id == question_to_delete.asked_by_id:
                    if advices_related_to_ques:
                        advices_related_to_ques.delete()
                    question_to_delete.delete()
                    resp_dict.update(message='Successfully deleted')
                    return Response(resp_dict, status=status.HTTP_204_NO_CONTENT)
                else:
                    resp_dict.update(message='Sorry this question was not asked by you', error=1)
                    return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
            except ObjectDoesNotExist:
                resp_dict.update(message='Question object not found. Did you provide a valid id?', error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            resp_dict.update(message='Not a valid user', error=1)
            return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
