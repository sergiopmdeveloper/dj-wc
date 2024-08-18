from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    """
    Custom user model
    """

    email = models.EmailField(
        unique=True, error_messages={"unique": "A user with that email already exists."}
    )

    def __str__(self) -> str:
        """
        String representation of the user

        Returns
        -------
        str
            The email of the user
        """

        return self.email

    class Meta:
        """
        Metadata options
        """

        db_table = "users"
        verbose_name_plural = "Users"
