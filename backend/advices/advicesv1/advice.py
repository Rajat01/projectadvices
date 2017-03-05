from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Advices
from serializers import AdviceSerializer



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
