import pytest
from rest_framework.test import APIClient
import json

from polls.models import Survey, Question


pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient


"""@pytest.mark.django_db
def test_list_survey(api_client):
    endpoint = "/api/v1/survey/"
    response = api_client().get(endpoint)
    assert response.status_code == 200"""


class TestSurvey:

    endpoint = '/api/v1/survey/'        #Много запросов
    enndpoint_1 = '/api/v1/survey/1/'   #Один запрос

    def test_list(self, api_client):

        survey = Survey(name="name1", description="description1")
        survey.save()

        response = api_client().get(self.endpoint)
        print(response.data["results"][0])      #Печатаем запрос в консоль
        assert response.status_code == 200      #Проверяем что запрос существует
        assert response.data["results"][0]["id"] == survey.id
        assert response.data["results"][0]["name"] == survey.name
        assert response.data["results"][0]["description"] == survey.description
 
        assert len(response.data) == 4
        assert isinstance(response.data, dict)
        assert isinstance(response.data["results"], list)
        assert isinstance(response.data["results"][0], dict)
        assert isinstance(response.data["results"][0]["id"], int)
        assert isinstance(response.data["results"][0]["name"], str)
        assert isinstance(response.data["results"][0]["description"], str)

        response_1 = api_client().get(self.enndpoint_1)
        print(response_1.data)
        
        assert response_1.status_code == 200    #Проверяем что запрос существует
        
        """response_2 = api_client().put(self.enndpoint_1)
        assert response_2.data["results"][0]["name"] == """



        



        







    """def test_detail(self, api_client):
        response = api_client().get(self.enndpoint_1)
        print(response.data)
    assert response.status_code == 200"""


class TestQuestion:

    enndpoint_2 = '/api/v1/question/'

    def test_choice(self, api_client):
        question = Question(question_text="How?")
        question.save()
        res = api_client().get(self.enndpoint_2)
        print(res.data["results"][0])
        assert res.status_code == 200
        assert question.question_text == res.data["results"][0]["question_text"]
