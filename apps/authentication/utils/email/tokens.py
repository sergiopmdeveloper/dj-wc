import datetime

import jwt
from django.conf import settings


class TokenError(Exception):
    """
    Custom token error exception
    """

    pass


class EmailConfirmationTokens:
    """
    Email confirmation tokens utility class
    """

    @staticmethod
    def generate_token(user_id: int) -> str:
        """
        Generates an email confirmation token

        Parameters
        ----------
        user_id : int
            The user id

        Returns
        -------
        str
            The email confirmation token
        """

        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.now() + datetime.timedelta(days=30),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def validate_token(token: str) -> int:
        """
        Validates an email confirmation token

        Parameters
        ----------
        token : str
            The email confirmation token

        Returns
        -------
        int
            The user id

        Raises
        ------
        TokenError
            If the token is invalid
        """

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            return payload["user_id"]
        except Exception:
            raise TokenError("Error validating token")
