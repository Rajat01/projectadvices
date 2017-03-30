from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from models import Comment
from serializers import CommentSerializer


@api_view(['POST'])
def post_comment(request, format=None):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if not request.user.is_anonymous:
                    serializer.save(commented_by=request.user)
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
def get_all_comments(request, story_id):
    resp_dict = dict(message='', error=0, result='')
    if request.method == 'GET':
        try:
            params = request.query_params
            page = int(params.get('page', 1))
            items_per_page = int(params.get('items_per_page', 5))
            min_offset = items_per_page * (page - 1)
            max_offset = items_per_page * page
            total_comments = Comment.objects.filter(story_id=story_id).count()
            all_comments = Comment.objects.filter(story_id=story_id).order_by('-id')[min_offset:max_offset]
            if all_comments:
                serializer = CommentSerializer(all_comments, many=True)
                resp_dict.update(message='Success', result=serializer.data, total_comments=total_comments)
                return Response(resp_dict, status=status.HTTP_200_OK)
            else:
                resp_dict.update(message='No comments found for this story', error=1)
                return Response(resp_dict, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print e
            resp_dict.update(message='Something went wrong', error=1)
            return Response(status=status.HTTP_400_BAD_REQUEST)
