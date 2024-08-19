import datetime

import jwt
from django.conf import settings


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
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
