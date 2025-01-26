from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    loginform, forget, otp, newpass, register, success,create_post,delete_post,
    loginsuccess, search, notifications, profile, changepass, messsages,change_profile_photo
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginform/', include('firstapp1.urls')),  # Ensure your app URLs are included here
    # Include other app URLs here, such as:
    path('', include('firstapp1.urls')),
    # path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
