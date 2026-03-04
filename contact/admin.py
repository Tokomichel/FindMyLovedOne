from django.contrib import admin
from .models import Contact, Code


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'first_phone', 'city')

# Register your models here.
admin.site.register(Contact, ContactAdmin)
admin.site.register(Code)