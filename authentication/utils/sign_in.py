from typing import Optional

from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser
from django.core.handlers.wsgi import WSGIRequest

from authentication.models import AppUser
from authentication.utils.abstract_authentication import AbstractAuthentication


class SignIn(AbstractAuthentication):
    """
    Sign in class

    Attributes
    ----------
    request : WSGIRequest
        The request object
    errors : list[str]
        The errors
    user : Optional[AbstractUser]
        The user

    Methods
    -------
    validate_data()
        Validates the sign in data
    validate_user()
        Validates the user credentials
    """

    def __init__(self, request: WSGIRequest) -> None:
        """
        Initializes the sign in object

        Parameters
        ----------
        request : WSGIRequest
            The request object
        """

        self.request = request
        self.errors = []
        self.user: Optional[AbstractUser] = None

    def validate_data(self) -> None:
        """
        Validates the sign in data
        """

        if not self.request.POST.get("email"):
            self.errors.append("Email is required.")

        if not self.request.POST.get("password"):
            self.errors.append("Password is required.")

    def validate_user(self) -> None:
        """
        Validates the user credentials
        """

        user = AppUser.objects.filter(email=self.request.POST.get("email")).first()

        if user:
            user = authenticate(
                self.request,
                username=user.username,
                password=self.request.POST.get("password"),
            )

        if not user:
            self.errors.append("Invalid credentials.")
            return

        self.user = user
