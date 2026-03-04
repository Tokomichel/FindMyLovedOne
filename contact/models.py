from django.db import models



# Create your models here.

class Contact(models.Model):
    login = models.CharField(max_length=120, default="")
    password = models.CharField(max_length=500, default="")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    first_phone = models.CharField(max_length=11)
    second_phone = models.CharField(max_length=11, blank=True,)
    city = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)


class Code(models.Model):
    contact = models.OneToOneField(Contact, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, unique=True)
    scan_count = models.PositiveIntegerField(default=0)