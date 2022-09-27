from statistics import mode

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, phone_number, password, second_name=None):
        if not email:
            raise ValueError("У пользователя должна быть электронная почта")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, second_name=second_name, phone_number=phone_number)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, name, phone_number, password, second_name=None):

        user = self.model(
            email=email,
            name=name,
            second_name=second_name,
            phone_number=phone_number,
            password=password,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255, null=True, default=None, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=30, unique=True, null=False, blank=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "phone_number",
    ]

    def get_full_name(self):
        return f"{self.name} {self.email}"

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
