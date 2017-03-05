from rest_framework import serializers
from models import Questions, Advices
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(source='id', required=False)

    class Meta:
        model = Questions
        fields = ('question_id', 'created', 'question', 'asked_by', 'upvote_by')


class AdviceSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Questions.objects.all(), required=True, source='question')
    advice_id = serializers.IntegerField(source='id',required=False)

    class Meta:
        model = Advices
        fields = ('advice_id', 'advice_content', 'question_id', 'advised_by', 'upvote_by', 'downvote_by')


# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vote
#         fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name')


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
