from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


@login_required(login_url="sign-in")
def home(request: WSGIRequest) -> HttpResponse:
    """
    The home view

    Parameters
    ----------
    request : WSGIRequest
        The request object

    Returns
    -------
    HttpResponse
        The rendered home page
    """

    return render(request, "base/home.html")
