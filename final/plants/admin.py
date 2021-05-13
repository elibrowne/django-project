from django.contrib import admin

from .models import Plant, Post, Profile

# Register your models here.
admin.site.register(Plant)
admin.site.register(Post)
admin.site.register(Profile)