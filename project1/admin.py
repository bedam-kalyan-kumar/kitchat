from django.contrib import admin
from .models import login, Post, Notification, Message, Comment, Like

admin.site.register(login)
admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Like)