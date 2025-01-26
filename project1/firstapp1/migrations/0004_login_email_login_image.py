# Generated by Django 5.0 on 2024-12-09 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp1', '0003_alter_login_password_alter_login_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='email',
            field=models.EmailField(blank=True, max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='login',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
