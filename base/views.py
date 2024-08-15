from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required(login_url="sign-in")
def home(request: HttpRequest) -> HttpResponse:
    """
    The home view

    Parameters
    ----------
    request : HttpRequest
        The request object

    Returns
    -------
    HttpResponse
        The rendered home page
    """

    return render(request, "base/home.html")
