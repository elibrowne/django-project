from django.contrib import admin

from .models import Plant, Post, Profile, Response

# Register your models here.
admin.site.register(Plant)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Response)