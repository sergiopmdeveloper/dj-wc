import pytest
from django.test import Client
from django.urls import reverse

from authentication.models import AppUser


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
