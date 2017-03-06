from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Questions, Advices
from serializers import QuestionSerializer, AdviceVoteSerializer


@api_view(['POST'])
def update_question_upvote_info(request, format=None):
    if request.method == 'POST':
        request_data = request.data
        question_id = request_data.get('question_id')
        question_obj = Questions.objects.get(pk=question_id)
        question_obj.upvote_by.add(request.user)
        serializer = QuestionSerializer(question_obj)
        return Response(serializer.data)



@api_view(['POST'])
def update_advice_vote_info(request, format=None):
    if request.method == 'POST':
        resp_dict = {}
        request_data = request.data
        advice_id = request_data.get('advice_id')
        advice_obj = Advices.objects.get(pk=advice_id)
        advice_upvote_users = advice_obj.upvote_by.all()
        advice_downvote_users = advice_obj.downvote_by.all()
        if request_data.get('entity_type') == 'upvote':
            if request.user not in advice_downvote_users:
                advice_obj.upvote_by.add(request.user)
                resp_dict['status_msg'] = 'Successfully updated upvote user'
                return Response(resp_dict)
            else:
                advice_downvote_users.remove(request.user)
                advice_obj.upvote_by.add(request.user)
                resp_dict['status_msg'] = 'Successfully updated upvote and downvote users list'
                return Response(resp_dict)
        elif request_data.get('entity_type') == 'downvote':
            advice_obj.downvote_by.add(request.user)
            resp_dict['status_msg'] = 'Successfully updated downvote user'
            return Response(resp_dict)
        else:
            resp_dict['err_msg'] = 'Please provide a valid entity_type'
            resp_dict['error'] = 1
            return Response(resp_dict)