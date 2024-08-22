from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse

from authentication.models import AppUser


def test_sign_up_get_success(client: Client):
    """
    Tests the GET method of the sign up view and checks if the
    response status code is 200 and the correct templates are used
    """

    response = client.get(reverse("sign-up"))
    templates = [template.name for template in response.templates]

    assert response.status_code == 200
    assert "page.html" in templates
    assert "authentication/sign-up.html" in templates


@pytest.mark.django_db
def test_sign_up_get_authenticated(client: Client):
    """
    Tests the GET method of the sign up view when the user is
    authenticated and checks if the response status code is 302
    """

    user = AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )
    client.force_login(user)

    response = client.get(reverse("sign-up"))

    assert response.status_code == 302


def test_sign_up_post_invalid_data(client: Client):
    """
    Tests the POST method of the sign up view with invalid data
    and checks if the response status code is 422 and the errors are returned
    """

    response = client.post(reverse("sign-up"), data={})

    assert response.status_code == 422
    assert response.json() == {
        "errors": [
            "Username is required.",
            "Email is required.",
            "Password is required.",
        ]
    }


@pytest.mark.django_db
def test_sign_up_post_invalid_credentials(client: Client):
    """
    Tests the POST method of the sign up view with invalid credentials
    and checks if the response status code is 422 and the errors are returned
    """

    AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )

    response = client.post(
        reverse("sign-up"),
        data={
            "username": "username",
            "email": "user@email.com",
            "password": "1234",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "errors": [
            "A user with that username already exists.",
            "A user with that email already exists.",
            "This password is too short. It must contain at least 8 characters.",
        ]
    }


@pytest.mark.django_db
def test_sign_up_post_success(client: Client):
    """
    Tests the POST method of the sign up view with valid credentials
    and checks if the response status code is 204, the user is created
    with is active and email confirmed set to False and the email is sent
    """

    with patch(
        "authentication.views.EmailConfirmationSender.send_email"
    ) as mock_send_email:
        response = client.post(
            reverse("sign-up"),
            data={
                "username": "username",
                "email": "user@email.com",
                "password": "secret1234",
            },
        )
    user = AppUser.objects.get(username="username")

    assert response.status_code == 204
    assert user.is_active is False
    assert user.email_confirmed is False
    mock_send_email.assert_called_once()
