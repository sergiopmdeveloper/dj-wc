from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class SignInView(View):
    """
    The sign in view
    """

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

        return render(request, "authentication/sign-in.html")
