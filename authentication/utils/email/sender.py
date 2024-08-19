from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from authentication.models import AppUser
from authentication.utils.email.tokens import EmailConfirmationTokens


class EmailConfirmationSender:
    """
    Email confirmation sender utility class
    """

    @staticmethod
    def send_email(request: WSGIRequest, user: AppUser) -> None:
        """
        Sends an email to the user with a
        link to activate their account

        Parameters
        ----------
        request : WSGIRequest
            The request object
        user : AppUser
            The user
        """

        current_site = get_current_site(request)
        mail_subject = "Activate your account!"

        message = render_to_string(
            "authentication/activate-your-account.html",
            {
                "domain": current_site.domain,
                "token": EmailConfirmationTokens.generate_token(user_id=user.id),
            },
        )

        email = EmailMessage(mail_subject, message, to=[user.email])

        email.send()
