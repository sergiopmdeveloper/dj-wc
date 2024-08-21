from typing import Optional

from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.handlers.wsgi import WSGIRequest

from authentication.models import AppUser
from authentication.utils.auth.abstract_authentication import AbstractAuthentication


class SignUp(AbstractAuthentication):
    """
    Sign up class

    Attributes
    ----------
    request : WSGIRequest
        The request object
    errors : list[str]
        The errors
    user : Optional[AppUser]
        The user

    Methods
    -------
    validate_data()
        Validates the sign up data
    validate_user()
        Validates the user credentials
    """

    def __init__(self, request: WSGIRequest) -> None:
        """
        Initializes the sign up object

        Parameters
        ----------
        request : WSGIRequest
            The request object
        """

        self._request = request
        self.errors = []
        self.user: Optional[AppUser] = None

    def validate_data(self) -> None:
        """
        Validates the sign up data
        """

        if not self._request.POST.get("username"):
            self.errors.append("Username is required.")

        if not self._request.POST.get("email"):
            self.errors.append("Email is required.")

        if not self._request.POST.get("password"):
            self.errors.append("Password is required.")

    def validate_user(self) -> None:
        """
        Validates the user credentials
        """

        user = AppUser(
            username=self._request.POST.get("username"),
            email=self._request.POST.get("email"),
            password=self._request.POST.get("password"),
        )

        try:
            user.full_clean()
        except ValidationError as e:
            self.errors.extend(e.messages)

        try:
            validate_password(self._request.POST.get("password"))
        except ValidationError as e:
            self.errors.append(list(e.messages)[0])

        if not self.errors:
            user.password = make_password(user.password)
            user.is_active = False
            self.user = user
