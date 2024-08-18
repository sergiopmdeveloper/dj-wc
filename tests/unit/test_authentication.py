import pytest
from django.test import RequestFactory

from authentication.models import AppUser
from authentication.utils.sign_in import SignIn


def test_sign_in_init(rf: RequestFactory):
    """
    Tests the __init__ method of the SignIn class
    and checks if the attributes are set correctly
    """

    request = rf.post("/sign-in")
    sign_in = SignIn(request=request)

    assert sign_in.request == request
    assert sign_in.errors == []
    assert sign_in.user is None


def test_sign_in_validate_data(rf: RequestFactory):
    """
    Tests the validate_data method of the SignIn class
    and checks if the errors are set correctly
    """

    request = rf.post("/sign-in", data={})
    sign_in = SignIn(request=request)

    sign_in.validate_data()

    assert sign_in.errors == ["Email is required.", "Password is required."]


@pytest.mark.django_db
def test_sign_in_validate_user_invalid_credentials(rf: RequestFactory):
    """
    Tests the validate_user method of the SignIn class with invalid
    credentials and checks if the errors are set correctly and the user is None
    """

    request = rf.post(
        "/sign-in", data={"email": "username@email.com", "password": "password"}
    )
    sign_in = SignIn(request=request)

    sign_in.validate_user()

    assert sign_in.errors == ["Invalid credentials."]
    assert sign_in.user is None


@pytest.mark.django_db
def test_sign_in_validate_user_valid_credentials(rf: RequestFactory):
    """
    Tests the validate_user method of the SignIn class with valid
    credentials and checks if the errors are empty and the user is set correctly
    """

    user = AppUser.objects.create_user(
        username="username", email="username@email.com", password="password"
    )
    request = rf.post(
        "/sign-in", data={"email": "username@email.com", "password": "password"}
    )
    sign_in = SignIn(request=request)

    sign_in.validate_user()

    assert sign_in.errors == []
    assert sign_in.user == user
