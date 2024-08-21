from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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

        protocol = "https" if request.is_secure() else "http"
        current_site = get_current_site(request)

        html_message = render_to_string(
            "authentication/activate-your-account.html",
            {
                "protocol": protocol,
                "domain": current_site.domain,
                "token": EmailConfirmationTokens.generate_token(user_id=user.id),
            },
        )

        text_message = strip_tags(html_message)
        mail_subject = "Activate your account!"

        email = EmailMultiAlternatives(
            subject=mail_subject,
            body=text_message,
            to=[user.email],
        )

        email.attach_alternative(html_message, "text/html")

        email.send()
