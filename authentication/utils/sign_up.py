from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.core.handlers.wsgi import WSGIRequest

from authentication.utils.abstract_authentication import AbstractAuthentication


class SignUp(AbstractAuthentication):
    """
    Sign up class

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
        Validates the sign up data
    validate_user()
        TODO: Validate user credentials using the AppUser model
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
        self.user: Optional[AbstractUser] = None

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
        TODO: Validate user credentials using the AppUser model
        """

        pass
