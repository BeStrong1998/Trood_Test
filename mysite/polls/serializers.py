
from polls.models import Question, Choice
from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    polls = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())
    owner = serializers.ReadOnlyField(source='owner_username')


    class Meta:
        model = User
        fields = ['id', 'username', 'polls', 'owner']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['pub_date', 'question_text']


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Choice
        fields = ['question', 'choice_text', 'votes']