from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=36, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    is_verified = models.BooleanField(default=False)
    news_count = models.IntegerField(default=0, blank=True)


class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

