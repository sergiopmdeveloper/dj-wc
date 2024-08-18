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
    Tests the GET method of the sign in view when the user is authenticated
    and checks if the response status code is 302 and the user is redirected
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
