from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from utils.email.strategies.abstract import EmailStrategyAbstract
from utils.tokens.tokens import Tokens

TEMPLATE = "authentication/activate-your-account.html"
SUBJECT = "Activate your account!"


class EmailConfirmationStrategy(EmailStrategyAbstract):
    """
    Email confirmation strategy
    """

    @staticmethod
    def send(to: str, **kwargs) -> None:
        """
        Sends an email to the user with a
        link to activate their account

        Parameters
        ----------
        to : str
            The recipient's email address
        **kwargs : dict
            Arbitrary keyword arguments. May include:
            - request (WSGIRequest) : The request object
            - user_id (int) : The user id
        """

        request: WSGIRequest = kwargs["request"]
        user_id: int = kwargs["user_id"]

        view_context = {
            "protocol": "https" if request.is_secure() else "http",
            "domain": get_current_site(request).domain,
            "token": Tokens.generate_token(user_id=user_id),
        }

        html_message = render_to_string(TEMPLATE, view_context)
        text_message = strip_tags(html_message)

        email = EmailMultiAlternatives(
            subject=SUBJECT,
            body=text_message,
            to=[to],
        )

        email.attach_alternative(html_message, "text/html")

        email.send()
