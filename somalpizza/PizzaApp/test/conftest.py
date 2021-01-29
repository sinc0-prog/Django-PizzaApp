from django.test import Client
import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user_data():
    return {'username': 'test1', 'password': 'test1234',
            'repeat_password': 'test1234', 'first_name': 'test_name',
            'last_name': 'last_test', 'email': 'email@email.com'}


@pytest.fixture
def client():
    client = Client()
    return client
