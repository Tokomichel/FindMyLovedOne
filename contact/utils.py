import jwt
from functools import wraps
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

def token_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return Response(data={"message": "Missing authorization header"}, status=status.HTTP_400_BAD_REQUEST)

        token = auth_header.split(' ')[1] #On extrait le token en retirant le "bearer"


        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.data["user_id"] = payload.get("user_id")

        except jwt.ExpiredSignatureError:
            return Response(data={"message": "Le token a expiré. Veuillez vous reconnecter"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response(data={"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(request, *args, **kwargs)
    return wrapper