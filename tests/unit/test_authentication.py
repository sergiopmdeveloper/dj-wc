import pytest
from django.test import RequestFactory

from authentication.models import AppUser
from authentication.utils.sign_in import SignIn
from authentication.utils.sign_up import SignUp


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


def test_sign_up_init(rf: RequestFactory):
    """
    Tests the __init__ method of the SignUp class
    and checks if the attributes are set correctly
    """

    request = rf.post("/sign-up")
    sign_up = SignUp(request=request)

    assert sign_up._request == request
    assert sign_up.errors == []
    assert sign_up.user is None


def test_sign_up_validate_data(rf: RequestFactory):
    """
    Tests the validate_data method of the SignUp class
    and checks if the errors are set correctly
    """

    request = rf.post("/sign-up", data={})
    sign_up = SignUp(request=request)

    sign_up.validate_data()

    assert sign_up.errors == [
        "Username is required.",
        "Email is required.",
        "Password is required.",
    ]


@pytest.mark.django_db
def test_sign_up_validate_user_invalid_credentials(rf: RequestFactory):
    """
    Tests the validate_user method of the SignUp class with invalid
    credentials and checks if the errors are set correctly and the user is None
    """

    AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )
    request = rf.post(
        "/sign-up",
        data={
            "username": "username",
            "email": "user@email.com",
            "password": "1234",
        },
    )
    sign_up = SignUp(request=request)

    sign_up.validate_user()

    assert sign_up.errors == [
        "A user with that username already exists.",
        "A user with that email already exists.",
        "This password is too short. It must contain at least 8 characters.",
    ]
    assert sign_up.user is None


@pytest.mark.django_db
def test_sign_up_validate_user_valid_credentials(rf: RequestFactory):
    """
    Tests the validate_user method of the SignUp class with valid
    credentials and checks if the errors are empty and the user is set correctly
    """

    request = rf.post(
        "/sign-up",
        data={
            "username": "username",
            "email": "user@email.com",
            "password": "secret1234",
        },
    )
    sign_up = SignUp(request=request)

    sign_up.validate_user()

    assert sign_up.errors == []
    assert sign_up.user is not None
