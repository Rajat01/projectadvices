from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Advices
from serializers import AdviceSerializer
from rest_framework import status


@api_view(['POST'])
def create_advice(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        request_data = request.data
        print request_data
        serializer = AdviceSerializer(data=request_data)
        question_id = request_data.get('question_id')
        question_obj = Advices.objects.filter(question_id=question_id)
        if question_obj:
            if serializer.is_valid():
                try:
                    if not request.user.is_anonymous:
                        serializer.save()
                        serializer.save(advised_by=request.user)
                        resp_dict.update(message='Success', result=serializer.data)
                        return Response(resp_dict, status=status.HTTP_201_CREATED)
                    else:
                        resp_dict.update(message='Please provide a valid user', error=1)
                        return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    print e
                    resp_dict.update(message='Something went wrong', error=1)
                    return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
            else:
                resp_dict.update(message='missing some required fields please check request', error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            resp_dict.update(message='Please enter a valid question', error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_advices(request, pk, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'GET':
        advices = Advices.objects.filter(question_id=pk)
        if advices:
            serializer = AdviceSerializer(advices, many=True)
            resp_dict.update(message='Success', result=serializer.data)
            return Response(resp_dict, status=status.HTTP_200_OK)
        else:
            resp_dict.update(message='No advices found for this question', error=1)
            return Response(resp_dict, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_advice_question(request, pk):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'DELETE':
        advice_to_delete = Advices.objects.get(pk=pk)
        if advice_to_delete:
            if request.user.id == advice_to_delete.advised_by_id:
                advice_to_delete.delete()
                resp_dict.update(message='Success')
                return Response(resp_dict, status=status.HTTP_204_NO_CONTENT)
            else:
                resp_dict.update(message='Please provide a valid user', error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            resp_dict.update(message='No advices to delete')
            return Response(resp_dict, status=status.HTTP_404_NOT_FOUND)
