from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache

from .models import AppUser


class SignInView(View):
    """
    The sign in view
    """

    @method_decorator(never_cache)
    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Renders the sign in page

        Parameters
        ----------
        request : HttpRequest
            The request object

        Returns
        -------
        HttpResponse
            The rendered sign in page
        """

        if request.user.is_authenticated:
            return redirect("home")

        return render(request, "authentication/sign-in.html")

    def post(self, request: HttpRequest) -> JsonResponse | HttpResponse:
        """
        Handles the sign in form submission

        Parameters
        ----------
        request : HttpRequest
            The request object

        Returns
        -------
        JsonResponse | HttpResponse
            A JSON response if there are errors,
            otherwise a successfull HTTP response
        """

        email = request.POST.get("email")
        password = request.POST.get("password")

        errors = []

        if not email:
            errors.append("Email is required.")

        if not password:
            errors.append("Password is required.")

        if errors:
            return JsonResponse({"errors": errors}, status=422)

        user = AppUser.objects.filter(email=email).first()

        if user:
            user = authenticate(request, username=user.username, password=password)

        if not user:
            errors.append("Invalid credentials.")
            return JsonResponse({"errors": errors}, status=401)

        login(request, user)

        return HttpResponse(status=204)
