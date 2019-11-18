from django.contrib import admin
from .models import Post, Comment , todayemotion , search
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(todayemotion)
admin.site.register(search)