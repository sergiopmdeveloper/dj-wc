from unittest.mock import patch

import pytest
from django.test import RequestFactory
from django.urls import reverse

from authentication.models import AppUser
from authentication.utils.email.sender import EmailConfirmationSender


@pytest.mark.django_db
def test_email_confirmation_sender_email_sent(rf: RequestFactory):
    """
    Tests the send_email method of the EmailConfirmationSender
    class and checks if the email is sent correctly
    """

    request = rf.get(reverse("email-confirmation"))
    user = AppUser.objects.create_user(
        username="username", email="user@email.com", password="password"
    )

    with patch(
        "authentication.utils.email.sender.EmailMultiAlternatives.send"
    ) as mock_send:
        EmailConfirmationSender.send_email(request=request, user=user)

    mock_send.assert_called_once()
