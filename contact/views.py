
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status

from contact.models import Contact, Code
from contact.utils import token_required, verifier_password, create_jwt, validate_contact, hasher_chaine


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
        contact = Contact.objects.filter(login=req.data["login"])[0]
    except Contact.DoesNotExist:
        return Response(data={"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    correct_hash: bool = verifier_password(req.data["password"], contact.password)

    if not correct_hash:
        return Response(data={"message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

    #génération du token
    token = create_jwt(contact)

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

    codes = []

    for elt in code:
        codes.append(str(elt))
    return Response(data=codes, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_contact(request):

    if validate_contact(dict(request.data)):
        # On continue la procedure de création
        contact = Contact(**request.data)

        #Je hash le mot de passe
        hashed_password = hasher_chaine(contact.password)
        contact.password = hashed_password
        contact.save()
        token = create_jwt(contact)
        return Response(data={"message": "Opération goes successfully", "token": token}, status=status.HTTP_200_OK)

    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)






