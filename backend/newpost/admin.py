from django.contrib import admin
from .models import Post,Tag,Like,Comment,Notification,Follow

#Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Follow)
