from rest_framework import serializers
from models import Questions, Advices


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = '__all__'




class AdviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advices
        fields = '__all__'


