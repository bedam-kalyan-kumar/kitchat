from django.contrib import admin
from django.urls import path,include
from .views import (
    loginform, forget,toggle_like, otp, newpass, register, success, create_post, delete_post, chat,add_comment,share_post,
    loginsuccess, search, notifications, profile,delete_notification,restore_notification, changepass, message, change_profile_photo
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', loginform, name="loginform"),
    path('forget/', forget, name="forget"),
    path('otp/', otp, name="otp"),
    path('newpass/', newpass, name='newpass'),
    path('register/', register, name='register'),
    path('success/', success, name='success'),
    path('loginsuccess/', loginsuccess, name='loginsuccess'),
    path('search/', search, name='search'),
    path('notifications/', notifications, name='notifications'),
    path('profile/', profile, name='profile'),
    path('changepass/', changepass, name='changepass'),
    path('messages/', message, name='messages'),
    path('change_profile_photo/', change_profile_photo, name='change_profile_photo'),
    path('create_post/', create_post, name='create_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
    path('chat/<int:recipient_id>/', chat, name='chat'), # Fixed URL for dynamic recipient ID
    path('delete-notification/',delete_notification, name='delete-notification'),
    path('restore-notification/', restore_notification, name='restore-notification'),
     path('toggle_like/<int:post_id>/',toggle_like, name='toggle_like'),
    path('toggle_like/<int:post_id>/',toggle_like, name='toggle_like'),
    path('add_comment/<int:post_id>/',add_comment, name='add_comment'),
    path('share_post/<int:post_id>/',share_post, name='share_post'),
    # path('delete-comment/<int:comment_id>/',delete_comment, name='delete_comment'),

]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
