from django.db import models

class login(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=255,blank=True)
    image = models.ImageField(upload_to='profile/', blank=True, null=True)

    def __str__(self):
        return self.username

