
from polls.models import Question, Choice, Survey
from rest_framework import serializers

from django.contrib.auth.models import User


#class UserSerializer(serializers.ModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    #polls = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    owvner = serializers.ReadOnlyField(source='owvner_username')


    class Meta:
        model = User
        fields = ['id', 'username', 'owvner']



#class QuestionSerializer(serializers.ModelSerializer):
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'pub_date', 'question_text', 'survey', 'owvner']



#class ChoiceSerializer(serializers.ModelSerializer):
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'choice_text', 'votes']



#class SurveySerializer(serializers.ModelSerializer):
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'name', 'description', 'owvner']
