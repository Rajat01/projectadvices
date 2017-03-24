from rest_framework import serializers
from models import Story, Comment
from django.contrib.auth.models import User

class CommonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, obj):
        return obj.username


class StorySerializer(serializers.ModelSerializer):
    is_anonymously_posted = serializers.BooleanField(required=True)
    created_by = CommonUserSerializer(read_only=True)
    story_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Story
        fields = ('story_id', 'story', 'created_by', 'is_anonymously_posted')
        # fields = '__all__'


class StoryPaginationSerializer(serializers.ModelSerializer):
    created_by = CommonUserSerializer(read_only=True)
    upvoted_by = CommonUserSerializer(read_only=True, many=True)
    downvoted_by = CommonUserSerializer(read_only=True, many=True)

    class Meta:
        model = Story
        fields = ('story', 'created_by', 'upvoted_by', 'downvoted_by', 'is_anonymously_posted')


class StoryVoteSerializer(serializers.ModelSerializer):
    story_id = serializers.IntegerField(source='id', required=True)
    created_by = CommonUserSerializer(read_only=True)
    upvoted_by = CommonUserSerializer(read_only=True, many=True)
    downvoted_by = CommonUserSerializer(read_only=True, many=True)

    class Meta:
        model = Story
        fields = ('story_id', 'created_by', 'upvoted_by', 'downvoted_by', 'is_anonymously_posted')


class CommentSerializer(serializers.ModelSerializer):
    story_id = serializers.PrimaryKeyRelatedField(queryset=Story.objects.all(), source='story', required=True)
    commented_by = CommonUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('comment', 'story_id', 'commented_by')
