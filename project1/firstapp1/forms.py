# forms.py
from django import forms
from .models import login
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = login
        fields = ['username', 'password','image']
        widgets = {
            'password': forms.PasswordInput(),  # To hide the password input
        }
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = SomeModel
#         fields = '__all__'