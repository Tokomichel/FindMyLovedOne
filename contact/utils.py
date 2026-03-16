import datetime

import bcrypt
import jwt
from functools import wraps
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import  Contact


def validate_contact(contact: dict):
    if "first_name" not in contact \
            or "last_name" not in contact \
            or "email" not in contact \
            or "first_phone" not in contact \
            or "city" not in contact \
            or "email" not in contact \
            or "password" not in contact \
            or "login" not in contact \
            or "adresse" not in contact:
        return False
    return True

def hasher_chaine(password: str) -> str:

    chaine_encode = password.encode("utf-8")

    resultat_hash = bcrypt.hashpw(chaine_encode, bcrypt.gensalt())

    return resultat_hash.decode("utf-8")

def verifier_password(chaine_claire: str, chaine_hashee: str) -> bool:
    chaine_encode = chaine_claire.encode("utf-8")
    chaine_hashee_encode = chaine_hashee.encode("utf-8")

    return bcrypt.checkpw(chaine_encode, chaine_hashee_encode)

def create_jwt(contact: Contact) -> str:
    # logic jwt
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    expiration = maintenant + datetime.timedelta(days=7)

    payload = {
        "user_id": contact.id,
        "login": contact.login,
        "exp": expiration,
        "iat": maintenant,
    }

    # génération du token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return token

def token_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response(data={"message": "Missing authorization header"}, status=status.HTTP_400_BAD_REQUEST)

        token = auth_header.split(' ')[1] #On extrait le token en retirant le "bearer".


        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.data["user_id"] = payload.get("user_id")

        except jwt.ExpiredSignatureError:
            return Response(data={"message": "Le token a expiré. Veuillez vous reconnecter"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response(data={"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(request, *args, **kwargs)
    return wrapper