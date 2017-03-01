from rest_framework import serializers
from models import Questions, Advices


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ('id', 'question')




class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advices
        fields = ('advice_content', 'question')


