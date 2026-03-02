from rest_framework import serializers
from .models import *
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answer = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id','text','answer']
        
class QuizSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, read_only =True)
    
    class Meta:
        model = Quiz
        fields = ['id','title','question']
