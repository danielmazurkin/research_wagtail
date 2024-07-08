from django.db import models
from django.contrib.auth.models import AbstractUser
from users.choices import ROLE_USER


class CustomUser(AbstractUser):
    """Пользовательский клас для определения роли пользователя в системе"""

    role = models.CharField(choices=ROLE_USER,
                            verbose_name="Роль пользователя",
                            max_length=255)