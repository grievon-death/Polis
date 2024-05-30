from django.contrib.auth.models import User
from django.db import models


class Profile(User):
    username = None
    document = models.TextField(
        null=False,
        blank=False,
        unique=True,
        help_text='Documento único de identificação do perfil.',
    )
