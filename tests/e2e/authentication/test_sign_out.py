import pytest
from django.test import Client
from django.urls import reverse

from authentication.models import AppUser


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
