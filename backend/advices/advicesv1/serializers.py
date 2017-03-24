from rest_framework import serializers
from models import Questions, Advices
from django.contrib.auth.models import User


class CommonUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, obj):
        return obj.username


class UserInfoQuestionSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(source='id', required=False)
    asked_by = CommonUserSerializer(read_only=True)
    upvote_by = CommonUserSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ('question_id', 'created', 'question', 'asked_by', 'upvote_by', 'is_anonymously_asked')


class QuestionSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(source='id', required=False)
    is_anonymously_asked = serializers.BooleanField(required=True)

    class Meta:
        model = Questions
        fields = ('question_id', 'created', 'question', 'asked_by', 'upvote_by', 'is_anonymously_asked')


class QuestionVoteSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(source='id', required=False)
    asked_by = CommonUserSerializer(read_only=True)
    upvote_by = CommonUserSerializer(many=True, read_only=True)

    class Meta:
        model = Questions
        fields = ('question_id', 'question', 'asked_by', 'upvote_by')


class UserInfoAdviceSerializer(serializers.ModelSerializer):
    advice_id = serializers.IntegerField(source='id', required=False)
    advised_by = CommonUserSerializer(read_only=True)
    upvote_by = CommonUserSerializer(many=True, read_only=True)
    downvote_by = CommonUserSerializer(many=True, read_only=True)

    class Meta:
        model = Advices
        fields = ('advice_id', 'advice_content', 'question_id', 'advised_by', 'upvote_by', 'downvote_by')


class AdviceSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Questions.objects.all(), required=True, source='question')
    advice_id = serializers.IntegerField(source='id', required=False)
    advised_by = CommonUserSerializer(read_only=True)

    class Meta:
        model = Advices
        fields = ('advice_id', 'advice_content', 'question_id', 'advised_by')


class AdviceVoteSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(queryset=Questions.objects.all(), required=False,
                                                     source='question')
    advice_id = serializers.IntegerField(source='id', required=True)
    upvote_by = CommonUserSerializer(many=True, read_only=True)
    downvote_by = CommonUserSerializer(many=True, read_only=True)

    class Meta:
        model = Advices
        fields = ('advice_id', 'advice_content', 'upvote_by', 'downvote_by', 'question_id')
