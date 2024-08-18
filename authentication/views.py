from django.contrib.auth import login
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from authentication.utils.sign_in import SignIn


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
