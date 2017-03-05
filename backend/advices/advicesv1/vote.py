from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Questions
from serializers import QuestionSerializer


@api_view(['POST'])
def update_question_upvote_info(request, format=None):
    if request.method == 'POST':
        request_data = request.data
        question_id = request_data.get('question_id')
        question_obj = Questions.objects.get(pk=question_id)
        question_obj.upvote_by.add(request.user)
        new_info = Questions.objects.get(pk=question_id)
        serializer = QuestionSerializer(new_info)
        return Response(serializer.data)
