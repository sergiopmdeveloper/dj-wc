import datetime
from typing import Optional

import jwt
from django.conf import settings

from utils.tokens.constants import DEFAULT_EXPIRATION_DAYS
from utils.tokens.exceptions import TokenValidationError


class Tokens:
    """
    Tokens utility class
    """

    @staticmethod
    def generate_token(
        data: Optional[dict[str, any]] = None, expiration_days: Optional[int] = None
    ) -> str:
        """
        Generates a token

        Parameters
        ----------
        data : Optional[dict[str, any]]
            The data to include in the token

        Returns
        -------
        str
            The generated token
        """

        expiration_days = DEFAULT_EXPIRATION_DAYS or 30

        payload = {
            "exp": datetime.datetime.now() + datetime.timedelta(days=expiration_days),
        }

        if data:
            payload.update(data)

        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def validate_token(token: str) -> dict[str, any]:
        """
        Validates a token

        Parameters
        ----------
        token : str
            The token

        Returns
        -------
        dict[str, any]
            The token payload

        Raises
        ------
        TokenValidationError
            If the token is invalid
        """

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            return payload
        except Exception:
            raise TokenValidationError("Error validating token")
