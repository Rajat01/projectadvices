from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Questions, Advices
from serializers import QuestionSerializer, AdviceVoteSerializer
from rest_framework import status
from django.contrib.auth.models import User


@api_view(['POST'])
def update_question_upvote_info(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        request_data = request.data
        question_id = request_data.get('question_id')
        try:
            if question_id:
                if not request.user.is_anonymous:
                    question_obj = Questions.objects.get(pk=question_id)
                    question_obj.upvote_by.add(request.user)
                    serializer = QuestionSerializer(question_obj)
                    resp_dict.update(message='Success', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    resp_dict.update(message='Not a valid user')
                    return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
            else:
                resp_dict.update(message='Please provide a valid question_id', error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            resp_dict.update(message='Something went wrong', error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_advice_vote_info(request, format=None):
    if request.method == 'POST':
        resp_dict = dict(message='', error=0, result='')
        request_data = request.data
        advice_id = request_data.get('advice_id')
        advice_obj = Advices.objects.get(pk=advice_id)
        advice_upvoted_by = advice_obj.upvote_by.all()
        advice_downvoted_by = advice_obj.downvote_by.all()
        if not request.user.is_anonymous:
            if request_data.get('entity_type') == 'upvote':
                if request.user not in advice_downvoted_by:
                    advice_obj.upvote_by.add(request.user)
                    serializer = AdviceVoteSerializer(advice_obj)
                    resp_dict.update(message='Successfully updated upvote user', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    advice_obj.downvote_by.remove(request.user)
                    advice_obj.upvote_by.add(request.user)
                    serializer = AdviceVoteSerializer(advice_obj)
                    resp_dict.update(message='Successfully removed from downvote and updated upvote user', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
            elif request_data.get('entity_type') == 'downvote':
                if request.user not in advice_upvoted_by:
                    advice_obj.downvote_by.add(request.user)
                    serializer = AdviceVoteSerializer(advice_obj)
                    resp_dict.update(message='Successfully updated downvote user', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    advice_obj.upvote_by.remove(request.user)
                    advice_obj.downvote_by.add(request.user)
                    serializer = AdviceVoteSerializer(advice_obj)
                    resp_dict.update(message='Successfully removed from upvote and updated downvote user', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
            else:
                resp_dict['err_msg'] = 'Please provide a valid entity_type'
                resp_dict['error'] = 1
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            resp_dict.update(message='Please provide a valid user', error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)