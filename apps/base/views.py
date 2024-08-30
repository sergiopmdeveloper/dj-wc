from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render


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
