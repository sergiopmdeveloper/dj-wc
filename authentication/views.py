from django.contrib.auth import login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from authentication.models import AppUser
from authentication.utils.sign_in import SignIn
from authentication.utils.sign_up import SignUp


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
            Redirects to the home page if the user is authenticated,
            otherwise renders the sign in page
        """

        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "authentication/sign-in.html")

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
            Redirects to the home page if the user is authenticated,
            otherwise renders the sign up page
        """

        if request.user.is_authenticated:
            return redirect("home")

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

        if not user or user.is_active:
            return redirect("sign-in")

        return render(
            request, "authentication/email-confirmation.html", {"email": email}
        )


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
