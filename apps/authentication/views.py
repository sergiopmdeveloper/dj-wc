from django.contrib.auth import login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from apps.authentication.models import AppUser
from apps.authentication.utils.auth.sign_in import SignIn
from apps.authentication.utils.auth.sign_up import SignUp
from utils.email.context import EmailContext
from utils.email.strategies.email_confirmation import EmailConfirmationStrategy
from utils.tokens.exceptions import TokenValidationError
from utils.tokens.tokens import Tokens

email_confirmation = EmailContext(strategy=EmailConfirmationStrategy)


class SignInView(View):
    """
    The sign in view
    """

    @method_decorator(never_cache)
    def get(self, request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
        """
        Renders the sign in page

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        HttpResponseRedirect | HttpResponse
            Redirects to the user page if the user is authenticated,
            otherwise renders the sign in page
        """

        if request.user.is_authenticated:
            return redirect("user")

        redirected = request.GET.get("next")

        return render(
            request, "authentication/sign-in.html", {"redirected": redirected}
        )

    def post(self, request: WSGIRequest) -> JsonResponse | HttpResponse:
        """
        Handles the sign in form submission

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        JsonResponse | HttpResponse
            A JSON response if there are errors,
            otherwise a successfull HTTP response
        """

        sign_in = SignIn(request=request)

        sign_in.validate_data()

        if sign_in.errors:
            return JsonResponse({"errors": sign_in.errors}, status=422)

        sign_in.validate_user()

        if sign_in.errors:
            return JsonResponse({"errors": sign_in.errors}, status=401)

        login(request, sign_in.user)

        return HttpResponse(status=204)


class SignUpView(View):
    """
    The sign up view
    """

    @method_decorator(never_cache)
    def get(self, request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
        """
        Renders the sign up page

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        HttpResponseRedirect | HttpResponse
            Redirects to the user page if the user is authenticated,
            otherwise renders the sign up page
        """

        if request.user.is_authenticated:
            return redirect("user")

        return render(request, "authentication/sign-up.html")

    def post(self, request: WSGIRequest) -> JsonResponse | HttpResponse:
        """
        Handles the sign up form submission

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        JsonResponse | HttpResponse
            A JSON response if there are errors,
            otherwise a successfull HTTP response
        """

        sign_up = SignUp(request=request)

        sign_up.validate_data()

        if sign_up.errors:
            return JsonResponse({"errors": sign_up.errors}, status=422)

        sign_up.validate_user()

        if sign_up.errors:
            return JsonResponse({"errors": sign_up.errors}, status=422)

        sign_up.user.save()

        email_confirmation.send(
            to=sign_up.user.email, request=request, user_id=sign_up.user.id
        )

        return HttpResponse(status=204)


class EmailConfirmationView(View):
    """
    The email confirmation view
    """

    def get(self, request: WSGIRequest) -> HttpResponseRedirect | HttpResponse:
        """
        Renders the email confirmation page

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        HttpResponseRedirect | HttpResponse
            Redirects to the sign in page if not user is found
            for the given email or the user is already active,
            otherwise renders the email confirmation page
        """

        email = request.GET.get("email")

        user = AppUser.objects.filter(email=email).first()

        if not user or user.email_confirmed:
            return redirect("sign-in")

        return render(
            request, "authentication/email-confirmation.html", {"email": email}
        )


class ActivateAccountView(View):
    """
    The activate account view
    """

    def get(self, request: WSGIRequest) -> HttpResponseRedirect:
        """
        Activates the user account

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        HttpResponseRedirect
            Redirects to the sign up page if the token is invalid or user is not found,
            redirects to the sign in page if the user is already active,
            otherwise signs in the user and redirects to the user page
        """

        token = request.GET.get("token")

        try:
            payload = Tokens.validate_token(token=token)
        except TokenValidationError:
            return redirect("sign-up")

        user = AppUser.objects.filter(id=payload["user_id"]).first()

        if not user:
            return redirect("sign-up")

        if user.email_confirmed:
            return redirect("sign-in")

        user.is_active = True
        user.email_confirmed = True
        user.save()

        login(request, user)

        response = redirect("user")
        response.set_cookie("accountActivated", "true")

        return response


class SignOutView(View):
    """
    The sign out view
    """

    def get(self, request: WSGIRequest) -> HttpResponse:
        """
        Signs out the user

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        HttpResponse
            A successfull HTTP response
        """

        logout(request)

        return HttpResponse(status=204)
