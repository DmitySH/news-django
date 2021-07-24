from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=36, blank=True)
    phone_number = models.CharField(max_length=12, blank=True)
    is_verified = models.BooleanField(default=False)
    news_count = models.IntegerField(default=0, blank=True)
