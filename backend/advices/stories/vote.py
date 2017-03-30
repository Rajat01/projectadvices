from models import Story
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from serializers import StoryVoteSerializer


@api_view(['POST'])
def update_story_vote_info(request, format=None):
    if request.method == 'POST':
        resp_dict = dict(message='', error=0, result='')
        request_data = request.data
        story_id = request_data.get('story_id')
        story_obj = Story.objects.get(pk=story_id)
        story_upvoted_by = story_obj.upvoted_by.all()
        story_downvoted_by = story_obj.downvoted_by.all()
        if not request.user.is_anonymous:
            if request_data.get('entity_type') == 'upvote':
                if request.user not in story_downvoted_by:
                    story_obj.upvoted_by.add(request.user)
                    serializer = StoryVoteSerializer(story_obj)
                    resp_dict.update(message='Successfully updated upvote user', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    story_obj.downvoted_by.remove(request.user)
                    story_obj.upvoted_by.add(request.user)
                    serializer = StoryVoteSerializer(story_obj)
                    resp_dict.update(message='Successfully removed from downvote and updated upvote user', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
            elif request_data.get('entity_type') == 'downvote':
                if request.user not in story_upvoted_by:
                    story_obj.downvoted_by.add(request.user)
                    serializer = StoryVoteSerializer(story_obj)
                    resp_dict.update(message='Successfully updated downvote user', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
                else:
                    story_obj.upvoted_by.remove(request.user)
                    story_obj.downvoted_by.add(request.user)
                    serializer = StoryVoteSerializer(story_obj)
                    resp_dict.update(message='Successfully removed from upvote and updated downvote user', result=serializer.data)
                    return Response(resp_dict, status=status.HTTP_201_CREATED)
            else:
                resp_dict.update(message='Please provide a valid entity_type', error=1)
                return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)
        else:
            resp_dict.update(message='Please provide a valid user', error=1)
            return Response(resp_dict, status=status.HTTP_400_BAD_REQUEST)