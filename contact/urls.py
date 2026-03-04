from django.contrib import admin
from django.urls import path
from .views import api_, api_endpoints, login, liste_code

urlpatterns = [
    path('api/', api_),
    path('view/', api_endpoints.as_view()),
    path('login/', login),
    path('liste_code/', liste_code),
]
