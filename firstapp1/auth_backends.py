from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.apps import apps

class LoginBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Dynamically get the 'login' model
        Login = apps.get_model('firstapp1', 'login')  # Replace 'firstapp1' with your app name
        try:
            user = Login.objects.get(username=username)
            # Verify the password
            if user and check_password(password, user.password):
                return user
        except Login.DoesNotExist:
            return None

    def get_user(self, user_id):
        Login = apps.get_model('firstapp1', 'login')
        try:
            return Login.objects.get(pk=user_id)
        except Login.DoesNotExist:
            return None
