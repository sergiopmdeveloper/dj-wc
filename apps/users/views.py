from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from apps.authentication.models import AppUser


class UserView(View):
    """
    The user view
    """

    @method_decorator(login_required(login_url="sign-in"))
    def get(self, request: WSGIRequest) -> HttpResponse:
        """
        Renders the user page

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        HttpResponse
            The rendered user page
        """

        account_activated = request.COOKIES.get("accountActivated")

        user = AppUser.objects.get(id=request.user.id)

        response = render(
            request,
            "users/user.html",
            {"account_activated": account_activated, "user": user},
        )

        if account_activated:
            response.delete_cookie("accountActivated")

        return response

    def post(self, request: WSGIRequest) -> HttpResponse:
        """
        Handles the user form submission

        Parameters
        ----------
        request : WSGIRequest
            The request object

        Returns
        -------
        HttpResponse
            A successfull HTTP response
        """

        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")

        user = AppUser.objects.get(id=request.user.id)

        if first_name != user.first_name:
            user.first_name = first_name

        if last_name != user.last_name:
            user.last_name = last_name

        user.save()

        return HttpResponse(status=200)
