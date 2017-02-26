from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from models import Questions
from serializers import AdviceSerializer




@api_view(['GET', 'POST'])
def question_list(request, format=None):

    """List all the questions"""

    if request.method == 'GET':
        question = Questions.objects.all()
        serializer = AdviceSerializer(question, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AdviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
