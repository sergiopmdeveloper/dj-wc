from django.urls import path

from apps.users import views

urlpatterns = [
    path("user", views.UserView.as_view(), name="user"),
]
