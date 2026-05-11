from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError


def validate_gmail(value):
    if not value.lower().endswith("@gmail.com"):
        raise ValidationError("Sirf @gmail.com email address allowed hai.")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, plain_password=None, **extra_fields):
        if not email:
            raise ValueError("Email zaroor dena hoga.")
        email = self.normalize_email(email)
        validate_gmail(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if plain_password:
            user.plain_password = plain_password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, validators=[validate_gmail])
    full_name = models.CharField(max_length=150, blank=True)
    plain_password = models.CharField(max_length=255, blank=True, verbose_name="Password (Plain)")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name or self.email
