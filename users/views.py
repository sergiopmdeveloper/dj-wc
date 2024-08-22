from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from authentication.models import AppUser


@login_required(login_url="sign-in")
def user(request: WSGIRequest) -> HttpResponse:
    """
    The user view

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
