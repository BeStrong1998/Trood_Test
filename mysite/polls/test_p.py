import pytest
from rest_framework.test import APIClient, APITestCase

from polls.models import Survey, Question, User


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient


"""@pytest.mark.django_db
def test_list_survey(api_client):
    endpoint = "/api/v1/survey/"
    response = api_client().get(endpoint)
    assert response.status_code == 200"""


class TestSurvey():

    endpoint = '/api/v1/survey/'        #Много запросов
    enndpoint_1 = '/api/v1/survey/1/'   #Один запрос

    def test_list(self, api_client):
        user = User.objects.create_user(username='admin', password='1234') #Создаём объект пользователя
        user.save() #добавляем в БД пользователя
        client = APIClient()
        client.login(username='admin', password='1234') #авторизуем нашего пользователя
        #client.get('/login/', {'username': 'admin', 'password': '1234'})
        survey = Survey(name="name1", description="description1", owvner=user) #создаём объект для модели Survey и присваиваем её полям значения
        survey.save() #Добавляем объект в БД

        response = api_client().get(self.endpoint)
        print(response.data[["results"][0]])
        assert response.status_code == 200
        assert User.objects.count() == 1
        print(User.objects.all())

        """print(response.data["results"][0])      #Печатаем запрос в консоль
        assert response.data["results"][0]["name"] == "name1"  #Проверяем значение в поле "name"
        assert response.status_code == 200      #Проверяем что запрос существует
        assert response.data["results"][0]["id"] == survey.id #Проверяем что поле "id" существует
        assert len(response.data) == 4
        assert isinstance(response.data, dict) #Проверяем что словарь
        assert isinstance(response.data["results"], list) #Проверяем что в ["results"] список
        assert isinstance(response.data["results"][0], dict) #Проверяем что в ["results"][0] словарь
        assert isinstance(response.data["results"][0]["id"], int) #Проверяем что в ["results"][0]["id"] число
        assert isinstance(response.data["results"][0]["name"], str) #Проверяем что в ["results"][0]["name"] строка"""

        """response_1 = api_client().get(self.enndpoint_1)
        print(response_1.data)

        assert response_1.status_code == 200    #Проверяем что запрос существует"""


class TestQuestion():

    enndpoint_2 = '/api/v1/question/'

    def test_choice(self, api_client):

        question = Question(question_text="How?")
        question.save()

        res = api_client().get(self.enndpoint_2)

        print(res.data["results"])
        assert res.status_code == 200
        assert question.question_text == res.data["results"][0]["question_text"]