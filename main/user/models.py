from django.db import models
from django.contrib.auth.models import AbstractUser
# updated user class with weight, height, age, and profilepic fields 
class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    age = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return self.username