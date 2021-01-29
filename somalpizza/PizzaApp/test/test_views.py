from django import urls
from django.contrib.auth import get_user_model
import pytest
from pytest import param
from pytest_django.fixtures import django_user_model

@pytest.mark.parametrize('param', [
    ('home'),
    ('login'),
    ('signup')
])

def test_public_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 200

@pytest.mark.django_db
def test_user_signup(client, user_data):
	user_model = get_user_model()
	assert user_model.objects.count() == 0
	signup_url = urls.reverse('signup')
	resp = client.post(signup_url, user_data)
	assert user_model.objects.count() == 1
	assert resp.status_code == 302




@pytest.mark.django_db
def test_user_login(client, user_data):
	login_url = urls.reverse('login')
	resp = client.post(login_url, user_data)
	assert resp.status_code == 302

@pytest.mark.parametrize('param', [
    ('create-special'),
    ('orders_list'),
    ('pizza_list_public'),
    ('cart-view'),
    ('update-adress'),
    ('change-password'),
    ('update-user')
])


def test_with_authenticated_client(client, django_user_model,param):
    username = "test1"
    password = "test1234"
    user = django_user_model.objects.create_user(username=username, password=password)
    temp_url = urls.reverse(param)
    client.login(username=username, password=password)
    response = client.get(temp_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_logout(client, django_user_model):
    username = "test1"
    password = "test1234"
    user = django_user_model.objects.create_user(username=username, password=password)
    logout_url = urls.reverse('logout-user')
    client.login(username=username, password=password)
    resp = client.get(logout_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse('home')