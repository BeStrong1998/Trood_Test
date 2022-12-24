import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(
        'date published', default=datetime.datetime.now())
    owvner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    survey = models.ForeignKey(
        'Survey', related_name='polls', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Survey(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    owvner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
