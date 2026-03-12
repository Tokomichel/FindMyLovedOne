from django.contrib import admin
from django.urls import path
from .views import api_, api_endpoints, login, liste_code, create_contact

urlpatterns = [
    path('api/', api_),
    path('create/', create_contact),
    path('login/', login),
    path('liste_code/', liste_code),
]
