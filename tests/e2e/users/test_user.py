import pytest
from django.test import Client
from django.urls import reverse

from authentication.models import AppUser


def test_user_info_get_unauthenticated(client: Client):
    """
    Tests the GET method of the user view when the user is
    unauthenticated and checks if the response status code is 302
    """

    response = client.get(reverse("user"))

    assert response.status_code == 302


@pytest.mark.django_db
def test_user_info_get_success(client: Client):
    """
    Tests the GET method of the user view when the user is
    authenticated and checks if the response status code is 200
    """

    user = AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )
    client.force_login(user)

    response = client.get(reverse("user"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_info_post_success(client: Client):
    """
    Tests the POST method of the user view and checks if the user
    information is updated successfully and the response status code is 200
    """

    user = AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )
    client.force_login(user)

    response = client.post(
        reverse("user"),
        {"first-name": "first_name", "last-name": "last_name"},
    )
    user.refresh_from_db()

    assert user.first_name == "first_name"
    assert user.last_name == "last_name"
    assert response.status_code == 200
