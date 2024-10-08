from django.db import models
from django.contrib.auth.models import User




class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,related_name='user_profile')
    bio=models.TextField()
    image=models.ImageField(upload_to='user_photos/',blank=True,null=True)
    def __str__(self):
            return f"{self.user.username}'s Profile"
