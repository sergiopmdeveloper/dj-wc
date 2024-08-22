import pytest

from authentication.utils.email.tokens import EmailConfirmationTokens, TokenError


def test_email_confirmation_tokens_generate_token():
    """
    Tests the generate_token function of the EmailConfirmationTokens
    class and checks if the token is generated correctly
    """

    token = EmailConfirmationTokens.generate_token(user_id=1)

    assert isinstance(token, str)


def test_email_confirmation_tokens_validate_token_invalid_token():
    """
    Tests the validate_token function of the EmailConfirmationTokens
    class with an invalid token and checks if the TokenError exception is raised
    """

    with pytest.raises(TokenError):
        EmailConfirmationTokens.validate_token(token="invalid_token")


def test_email_confirmation_tokens_validate_token_valid_token():
    """
    Tests the validate_token function of the EmailConfirmationTokens
    class with a valid token and checks if the user id is returned correctly
    """

    token = EmailConfirmationTokens.generate_token(user_id=1)

    user_id = EmailConfirmationTokens.validate_token(token=token)

    assert user_id == 1
