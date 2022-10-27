from django.contrib import admin
from .models import User, Song

# Register your models here.
admin.site.register(User)
admin.site.register(Song)