from rest_framework import serializers
from models import Questions


class AdviceSerializer(serializers.Serializer):
    class Meta:
        model = Questions
        fields = ('id', 'question')