from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Advices, Questions
from serializers import AdviceSerializer, AdviceVoteSerializer, UserInfoAdviceSerializer
from rest_framework import status


@api_view(['POST'])
def create_advice(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        request_data = request.data
        print request_data
        serializer = AdviceSerializer(data=request_data)
        question_id = request_data.get('question_id')
        question_obj = Questions.objects.get(id=question_id)
        try:
            if question_obj:
                if serializer.is_valid():
                    if not request.user.is_anonymous:
                        serializer.save(advised_by=request.user)
                        serializer.save()
                        resp_dict.update(message='Success', result=serializer.data)
                        return Response(resp_dict, status=status.HTTP_201_CREATED)
                    else:
                        resp_dict.update(message='Please provide a valid user', error=1)
                        return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
                else:
                    resp_dict.update(message='missing some required fields please check request', error=1)
                    return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
            else:
                resp_dict.update(message='Question does not exist', error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            resp_dict.update(message='Something went wrong', error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def update_advice(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        try:
            if not request.user.is_anonymous:
                request_data = request.data
                advice_id = request_data.get('advice_id', None)
                advice_to_update = Advices.objects.get(pk=advice_id)
                serializer = AdviceVoteSerializer(advice_to_update)
                if request.user.id == advice_to_update.advised_by_id:
                    advice_to_update.advice_content = request_data.get('advice_content')
                    advice_to_update.save(update_fields=['advice_content'])
                    resp_dict.update(result=serializer.data, message='Successfully updated advice')
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    resp_dict.update(message='Sorry this advice was not given by you', error=1)
                    return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
            else:
                resp_dict.update(message='Not a valid user', error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            resp_dict.update(message=str(e), error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_all_advices(request, question_id, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'GET':
        try:
            params = request.query_params
            page = int(params.get('page', 1))
            items_per_page = int(params.get('items_per_page', 5))
            min_offset = items_per_page * (page - 1)
            max_offset = items_per_page * page
            total_advices = Advices.objects.filter(question_id=question_id).count()
            advices = Advices.objects.filter(question_id=question_id).order_by('-id')[min_offset:max_offset]
            if advices:
                serializer = UserInfoAdviceSerializer(advices, many=True)
                resp_dict.update(message='Success', result=serializer.data, total_advices=total_advices)
                return Response(resp_dict, status=status.HTTP_200_OK)
            else:
                resp_dict.update(message='No advices found for this question', error=1)
                return Response(resp_dict, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            resp_dict.update(message='Something went wrong', error=1)


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
