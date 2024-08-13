from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def sign_in(request: HttpRequest) -> HttpResponse:
    """
    The sign in view

    Parameters
    ----------
    request : HttpRequest
        The request object

    Returns
    -------
    HttpResponse
        The rendered sign in page
    """

    return render(request, "authentication/sign-in.html")
