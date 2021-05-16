"""

"""
from datetime import datetime, timedelta
from typing import Optional, Tuple

from django.conf import settings
from django.contrib.auth.models import User
from jwt import encode


def generate_tokens(user: User) -> Tuple[Optional[str], Optional[str]]:
    """Use this function for generating the access and refresh tokens.

    This function is used for taking the user data and generating the access and the
    refresh tokens.

    :param user: the user data.
    :return: the access and refresh tokens.
    """
    if not isinstance(user, User):
        return None, None
    utc_now = datetime.now()
    access_payload = {
        "iat": utc_now,
        "exp": utc_now + timedelta(minutes=60),
        "nbf": utc_now,
        "iss": "http://localhost:8000/login",
        # this has to be replaced with application domain after deploying
        "username": user.username,
        "email": user.email,
        "type": "access",
    }
    access_token = encode(access_payload, settings.SECRET_KEY, algorithm="HS256")

    refresh_payload = {
        "iat": utc_now,
        "exp": utc_now + timedelta(days=2),
        "nbf": utc_now,
        "iss": "http://localhost:8000/login",
        # this has to be replaced with application domain after deploying
        "username": user.username,
        "type": "refresh",
    }

    refresh_token = encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")
    return access_token, refresh_token
