from rest_framework import serializers
from models import Questions, Advices
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
    asked_by = serializers.ReadOnlyField(source='asked_by.username')

    class Meta:
        model = Questions
        fields = ('id', 'created', 'question', 'up_votes', 'asked_by')


class AdviceSerializer(serializers.ModelSerializer):
    advised_by = serializers.ReadOnlyField(source='advised_by.username')

    class Meta:
        model = Advices
        fields = ('id', 'advice_content', 'question', 'up_votes', 'advised_by')


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
