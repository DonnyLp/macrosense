from django.db import models

# model for user
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    weight = models.IntegerField()
    height = models.IntegerField()
    age = models.IntegerField()
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True)

    def __str__(self):
        return self.name