from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse

from authentication.models import AppUser


def test_sign_in_get_success(client: Client):
    """
    Tests the GET method of the sign in view and checks if the
    response status code is 200 and the correct templates are used
    """

    response = client.get(reverse("sign-in"))
    templates = [template.name for template in response.templates]

    assert response.status_code == 200
    assert "page.html" in templates
    assert "authentication/sign-in.html" in templates


@pytest.mark.django_db
def test_sign_in_get_authenticated(client: Client):
    """
    Tests the GET method of the sign in view when the user is
    authenticated and checks if the response status code is 302
    """

    user = AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )
    client.force_login(user)

    response = client.get(reverse("sign-in"))

    assert response.status_code == 302


def test_sign_in_post_invalid_data(client: Client):
    """
    Tests the POST method of the sign in view with invalid data
    and checks if the response status code is 422 and the errors are returned
    """

    response = client.post(reverse("sign-in"), data={})

    assert response.status_code == 422
    assert response.json() == {
        "errors": ["Email is required.", "Password is required."]
    }


@pytest.mark.django_db
def test_sign_in_post_invalid_credentials(client: Client):
    """
    Tests the POST method of the sign in view with invalid credentials
    and checks if the response status code is 401 and the errors are returned
    """

    response = client.post(
        reverse("sign-in"), data={"email": "user@email.com", "password": "password"}
    )

    assert response.status_code == 401
    assert response.json() == {"errors": ["Invalid credentials."]}


@pytest.mark.django_db
def test_sign_in_post_success(client: Client):
    """
    Tests the POST method of the sign in view with valid credentials
    and checks if the response status code is 204 and the user is signed in
    """

    user = AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )

    response = client.post(
        reverse("sign-in"), data={"email": "user@email.com", "password": "password"}
    )

    assert response.status_code == 204
    assert client.session["_auth_user_id"] == str(user.id)


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


@pytest.mark.django_db
def test_email_confirmation_get_nonexistent_email(client: Client):
    """
    Tests the GET method of the email confirmation view with an
    email that does not exist and checks if the response status code is 302
    """

    response = client.get(reverse("email-confirmation") + "?email=user@email.com")

    assert response.status_code == 302


@pytest.mark.django_db
def test_email_confirmation_get_email_already_confirmed(client: Client):
    """
    Tests the GET method of the email confirmation view with an
    email that is already active and checks if the response status code is 302
    """

    AppUser.objects.create_user(
        username="username",
        email="user@email.com",
        password="password",
        email_confirmed=True,
    )
    response = client.get(reverse("email-confirmation") + "?email=user@email.com")

    assert response.status_code == 302


@pytest.mark.django_db
def test_email_confirmation_get_success(client: Client):
    """
    Tests the GET method of the email confirmation view with an
    email that is not active and checks if the response status code is 200
    """

    AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )
    response = client.get(reverse("email-confirmation") + "?email=user@email.com")

    assert response.status_code == 200


def test_activate_account_get_invalid_token(client: Client):
    """
    Tests the GET method of the activate account view with an
    invalid token and checks if the response status code is 302
    """

    response = client.get(reverse("activate-account") + "?token=invalid_token")

    assert response.status_code == 302


@pytest.mark.django_db
def test_activate_account_get_user_not_found(client: Client):
    """
    Tests the GET method of the activate account view with a token
    that does not match any user and checks if the response status code is 302
    """

    with patch(
        "authentication.views.EmailConfirmationTokens.validate_token",
        return_value=1,
    ):
        response = client.get(reverse("activate-account") + "?token=token")

    assert response.status_code == 302


@pytest.mark.django_db
def test_activate_account_get_email_already_confirmed(client: Client):
    """
    Tests the GET method of the activate account view with a token
    that matches a user with email already confirmed and checks if the
    response status code is 302
    """

    with (
        patch("authentication.views.EmailConfirmationTokens.validate_token"),
        patch("authentication.views.AppUser.objects") as mock_objects,
    ):
        mock_objects.filter.return_value.first.return_value = AppUser(is_active=True)
        response = client.get(reverse("activate-account") + "?token=token")

    assert response.status_code == 302


@pytest.mark.django_db
def test_activate_account_get_success(client: Client):
    """
    Tests the GET method of the activate account view with a token
    that matches a user with email not confirmed and checks if the
    response status code is 302, the user is signed in, the user is active,
    the email is confirmed and the accountActivated cookie is set to true
    """

    user = AppUser.objects.create_user(
        username="username",
        email="user@email.com",
        password="password",
        is_active=False,
        email_confirmed=False,
    )

    with (
        patch("authentication.views.EmailConfirmationTokens.validate_token"),
        patch("authentication.views.AppUser.objects") as mock_objects,
    ):
        mock_objects.filter.return_value.first.return_value = user
        response = client.get(reverse("activate-account") + "?token=token")

    assert response.status_code == 302
    assert client.session["_auth_user_id"] == str(user.id)
    assert user.is_active is True
    assert user.email_confirmed is True
    assert client.cookies.get("accountActivated").value == "true"


@pytest.mark.django_db
def test_sign_out_get_success(client: Client):
    """
    Tests the GET method of the sign out view and checks if the
    response status code is 204 and the user is signed out
    """

    user = AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )
    client.force_login(user)

    response = client.get(reverse("sign-out"))

    assert response.status_code == 204
    assert client.session.get("_auth_user_id") is None
