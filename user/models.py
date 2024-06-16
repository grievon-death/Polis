from django.contrib.auth.models import User
from django.db import models


class Profile(User):
    document = models.TextField(
        null=False,
        blank=False,
        unique=True,
        help_text='Documento único de identificação do perfil.',
    )


class TokenMap(models.Model):
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        help_text='Usuário qual pertence o token.',
    )
    token = models.TextField(
        null=False,
        blank=False,
        unique=True,
        help_text='Token de login.',
    )
