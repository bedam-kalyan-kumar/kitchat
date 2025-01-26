from django.db import models
from django.contrib.auth.models import AbstractUser


class login(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    image = models.ImageField(
        upload_to='profile_photos/',
        blank=True,
        null=True,
        default='profile_pics/default-profile.png'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    gmail = models.EmailField(max_length=254, unique=True)


    def __str__(self):
        return self.username



class Post(models.Model):
    user = models.ForeignKey(login, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    shares_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.user.username} ({self.id})"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Liked your post'),
        ('comment', 'Commented on your post'),
        ('follow', 'Followed you'),
        ('mention', 'Mentioned you'),
        ('message', 'Sent you a message'),
        ('post', 'Posted something'),
        ('profile', 'Updated their profile'),
    ]

    user = models.ForeignKey(
        login,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    triggered_by = models.ForeignKey(
        login,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='triggered_notifications'
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPES,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'

    class Meta:
        ordering = ['-timestamp']  # Latest notifications first


class Message(models.Model):
    sender_id = models.IntegerField()
    sender_username = models.CharField(max_length=255)
    recipient_id = models.IntegerField()
    recipient_username = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender_username} to {self.recipient_username}"


from django.contrib.auth.models import User

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
