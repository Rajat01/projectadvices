from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Story
from serializers import StorySerializer, StoryPaginationSerializer


@api_view(['POST'])
def post_story(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                if not request.user.is_anonymous:
                    serializer.save(created_by=request.user)
                    serializer.save()
                    resp_dict.update(result=serializer.data, message='Success')
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    resp_dict.update(message='Not a valid user', error=1)
                    return Response(resp_dict, status=status.HTTP_403_FORBIDDEN)
            except Exception as e:
                print e
                resp_dict.update(message=str(e), error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_stories(request):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'GET':
        try:
            params = request.query_params
            page = int(params.get('page', 1))
            items_per_page = int(params.get('items_per_page', 5))
            min_offset = items_per_page * (page - 1)
            max_offset = items_per_page * page
            total_stories = Story.objects.all().count()
            story_objs = Story.objects.all()[min_offset:max_offset]
            serializer = StoryPaginationSerializer(story_objs, many=True)
            resp_dict.update(result=serializer.data, total_stories=total_stories)
            return Response(resp_dict, status=status.HTTP_200_OK)
        except Exception as e:
            print e
            resp_dict.update(message=str(e), error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
# Create your views here.
