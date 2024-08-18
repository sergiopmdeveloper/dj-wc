from django.contrib import admin

from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    """
    App user admin
    """

    list_display = ("username", "email")
