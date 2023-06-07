from django.contrib import admin
from .models import Profile , Friend , Message , Image

# Register your models here.
admin.site.register([Profile , Friend , Message , Image])