from rest_framework import serializers
from models import Questions, Advices, Vote
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'created', 'question', 'asked_by')


class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advices
        fields = ('id', 'advice_content', 'question_id', 'advised_by')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('created', 'advice_id', 'question_id', 'upvote_count', 'downvote_count', 'entity_type', )

class QuesUserSerializer(serializers.ModelSerializer):
    question_user = serializers.PrimaryKeyRelatedField(many=True, queryset=Questions.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'question_user')


class AdvUserSerializer(serializers.ModelSerializer):
    advice_user = serializers.PrimaryKeyRelatedField(many=True, queryset=Advices.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'advice_user')
