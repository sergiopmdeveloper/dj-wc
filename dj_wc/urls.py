from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("", include("authentication.urls")),
    path("", include("users.urls")),
]
