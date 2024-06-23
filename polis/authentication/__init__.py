from datetime import datetime, timedelta

import jwt
from django.conf import settings

from user.models import Profile


class TokenManager:
    @staticmethod
    def generate_token(user: Profile) -> str:
        """
        Gera o token JWT.
        """
        _payload = {
            'user': user.username,
            'email': user.email,
            'superuser': user.is_superuser,
            'anonymous': user.is_anonymous,
            'exp': int((datetime.now() + timedelta(days=7)).timestamp()),
        }

        return jwt.encode(_payload, settings.SECRET_KEY)

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Decodifica o token.
        """
        try:
            _token = jwt.decode(token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            raise Exception({ 'error': 'Expired token!' })
        except Exception as e:
            raise e
