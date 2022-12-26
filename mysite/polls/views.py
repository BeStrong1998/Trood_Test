from rest_framework.response import Response
from rest_framework import response
from rest_framework import viewsets
from rest_framework import permissions
from polls.serializers import (
    QuestionSerializer, ChoiceSerializer, SurveySerializer)
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Survey
from django.contrib.auth.models import User, Group
from polls.serializers import UserSerializer, GroupSerialaizer
from rest_framework.decorators import action, api_view
from polls.permissions import IsOwnerOrReadOnly
from rest_framework.exceptions import APIException


class GroupViewset(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerialaizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all().order_by('name', 'description')
    serializer_class = SurveySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
        ]
    """чтобы все фрагменты кода были видны всем, но также чтобы убедиться,
    что только пользователь, создавший фрагмент кода,
    может обновить или удалить его."""

    def perform_create(self, serializer):
        serializer.save(owvner=self.request.user)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('pub_date', 'question_text')
    serializer_class = QuestionSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
        ]
    """чтобы все фрагменты кода были видны всем, но также чтобы убедиться,
        что только пользователь, создавший фрагмент кода,
        может обновить или удалить его."""

    def perform_create(self, serializer):
        serializer.save(owvner=self.request.user)
        """делает связать пользователя, создавшего фрагмент,
    с экземпляром фрагмента (Пользователь является автором)"""


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all().order_by(
        'question', 'choice_text', 'votes')
    serializer_class = ChoiceSerializer
    """ permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
        ]"""
    """чтобы все фрагменты кода были видны всем, но также чтобы убедиться,
        что только пользователь, создавший фрагмент кода,
        может обновить или удалить его."""

    @action(detail=True, methods=['get', 'post', 'put', 'patch'])
    def votes(self, request, pk=None):
        """raise APIException"""
        if request.method == 'GET':
            e = APIException
            e.status_code = 400
            raise e('Ошибка на сервере')

        """Если метод request возвращает запрос POST;
            Записываем в переменную -e- APIException;
            Далее говорим что e.status_code = 400;
            Объявляем ошибку raise e"""
        obj = self.get_object()
        obj.votes += 1
        obj.save()
        return response.Response({'votes': obj.votes})

    @action(detail=False, methods=['post', 'get'])
    def votes_get(self, request):
        if request.method == 'GET':
            raise APIException(404)
        else:
            return response.Response({'Можно вернуть что то дополнительно'})


@api_view(('POST', 'GET'))
def api(request):
    if request.method == 'GET':
        return Response({'status': '200'})
    else:
        request.method = 'POST'
        ex = APIException
        ex.status_code = 404
        raise ex({'detail': 'Сервер временно недоступен'})


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """ Return the last five published questions
        (not including those set to be
        published in the future).
        Верните последние 10 опубликованных вопросов (не включая те,
        которые будут
        опубликованы в будущем)"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            '-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """xcludes any questions that aren't published yet.
        Исключает любые вопросы, которые еще не опубликованы."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


"""@action(detail=False, methods=['post'])
   @api_view(['GET', 'POST'])"""


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Повторно отобразите форму голосования по вопросу.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Выберете ответ",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Всегда возвращайте HttpResponseRedirect после успешной обработки
        # с данными POST. Это предотвращает повторную публикацию данных, если
        # пользователь нажимает кнопку "Назад".
        return HttpResponseRedirect(reverse(
            'polls:results', args=[question.id]))

    """
class QuestionList(generics.ListCreateAPIView):
    #Конкретное представление для перечисления набора запросов
    # или создания экземпляра модели.
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    #Конкретное представление для извлечения, обновления
    # или удаления экземпляра модели.
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]"""
