import bcrypt
import jwt

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
import datetime

from contact.models import Contact, Code
from find import settings
from contact.utils import token_required


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



# Create your views here.

@api_view(['GET'])
def api_(req: Request):
    _data = {
        "message": "Hello World!"
    }
    return Response(data=_data, status=status.HTTP_200_OK)


# endpoint du login
@api_view(['POST'])
def login(req: Request):
    if "password" not in req.data or "login" not in req.data:
        return Response(data={"message": "Missing password or login"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        contact = Contact.objects.get(login=req.data["login"])
    except Contact.DoesNotExist:
        return Response(data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    correct_hash: bool = verifier_password(req.data["password"], contact.password)

    if not correct_hash:
        return Response(data={"message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

    #logic jwt
    maintenant = datetime.datetime.now(datetime.timezone.utc)
    expiration = maintenant + datetime.timedelta(days=7)

    payload = {
        "user_id": contact.id,
        "login": contact.login,
        "exp":expiration,
        "iat":maintenant,
    }

    #génération du token
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    _data = {
        "login": contact.login,
        "token": token,
        "message": "Successful login",
    }

    return Response(data=_data, status=status.HTTP_200_OK)

#liste des codes d'un contact

@api_view(['GET'])
@token_required
def liste_code(req: Request):

    contact = Contact.objects.get(id=req.data["user_id"])
    code = Code.objects.filter(contact=contact)

    codes = list()

    for elt in code:
        codes.append(str(elt))
    return Response(data=codes, status=status.HTTP_200_OK)


class api_endpoints(APIView):

    def post(self, request):
        print(request.data)
        if validate_contact(dict(request.data)):
            # On continue la procedure de création
            contact = Contact(**request.data)

            #Je hash le mot de passe
            hashed_password = hasher_chaine(contact.password)
            contact.password = hashed_password
            contact.save()
            return Response(data={"message": "Opération goes succesfully"}, status=status.HTTP_200_OK)

        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)






