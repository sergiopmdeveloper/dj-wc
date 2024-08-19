from django.urls import path

from . import views

urlpatterns = [
    path("sign-in", views.SignInView.as_view(), name="sign-in"),
    path("sign-up", views.SignUpView.as_view(), name="sign-up"),
    path(
        "email-confirmation",
        views.EmailConfirmationView.as_view(),
        name="email-confirmation",
    ),
    path(
        "activate-account", views.ActivateAccountView.as_view(), name="activate-account"
    ),
    path("sign-out", views.SignOutView.as_view(), name="sign-out"),
]
