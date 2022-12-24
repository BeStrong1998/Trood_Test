import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient


@pytest.mark.django_db
def test_list(api_client):
    endpoint = "/api/v1/survey/"
    response = api_client().get(endpoint)
    assert response.status_code == 200
