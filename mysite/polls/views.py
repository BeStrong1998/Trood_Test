from rest_framework import viewsets
from rest_framework import permissions
from polls.serializers import QuestionSerializer, ChoiceSerializer, SurveySerializer

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Survey

from django.contrib.auth.models import User
from polls.serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from polls.permissions import IsOwnerOrReadOnly



class UserList(generics.ListAPIView):
    """Конкретное представление для перечисления набора запросов."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """Конкретное представление для извлечения экземпляра модели."""
    queryset = User.objects.all()
    serializer_class = UserSerializer





class QuestionList(generics.ListCreateAPIView):
    """Конкретное представление для перечисления набора запросов или создания экземпляра модели."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    """Конкретное представление для извлечения, обновления или удаления экземпляра модели."""
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]





class SurveyList(generics.ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]




"""Набор представлений, который предоставляет действия по умолчанию `create()`, `retrieve()`, `update()`,
`partial_update()`, `destroy()` и `list()`."""
class SurveyViewSet(viewsets.ModelViewSet):
    """ Конечная точка API, которая позволяет просматривать или редактировать пользователей"""
    queryset = Survey.objects.all().order_by('name', 'description')
    serializer_class = SurveySerializer
    permission_classes = [permissions.IsAuthenticated]
    


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, которая позволяет просматривать или редактировать пользователей.
    """
    queryset = Question.objects.all().order_by('pub_date', 'question_text')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]



class ChoiceViewSet(viewsets.ModelViewSet):
    """
   Конечная точка API, которая позволяет просматривать или редактировать группы.
    """
    queryset = Choice.objects.all().order_by('question', 'choice_text', 'votes')
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    


"""from mysite.polls.serializers import QuestionSerialalizer
from rest_framework import generics (из mysite.polls.serializers импортируйте QuestionSerializer
из rest_framework импортируйте дженерики)"""

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        Верните последние пять опубликованных вопросов (не включая те, которые будут
        опубликованы в будущем)
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        Исключает любые вопросы, которые еще не опубликованы.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))