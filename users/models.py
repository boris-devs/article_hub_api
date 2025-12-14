from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_mongodb_backend.fields import ObjectIdAutoField
from users.managers import CustomUserManager


class User(AbstractUser):
    _id = ObjectIdAutoField(primary_key=True, editable=False)
    email = models.EmailField(_("email address"),unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email