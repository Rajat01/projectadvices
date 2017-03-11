from rest_framework import serializers
from models import Story, Comment
from django.contrib.auth.models import User


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('question_id', 'created', 'question', 'asked_by', 'upvote_by', 'is_anonymously_asked')


class CommentSerializer(serializers.ModelSerializer):
    story_id = serializers.PrimaryKeyRelatedField(source='story', read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('advice_id', 'advice_content', 'question_id', 'advised_by', 'upvote_by', 'downvote_by')
