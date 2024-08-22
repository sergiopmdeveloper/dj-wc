from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse

from authentication.models import AppUser


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
