from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

username_validator = RegexValidator(r"^[\w.@+-]+")


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user')
    ]
    username = models.CharField(
        max_length=150, unique=True, validators=[username_validator]
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField(
        blank=True
    )

    @property
    def is_moderator(self):
        """True для пользователей с правами модератора."""
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        """True для пользователей с правами админа и суперпользователей."""
        return self.role == User.ADMIN or self.is_staff or self.is_superuser
