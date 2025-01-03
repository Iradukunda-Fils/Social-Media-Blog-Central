from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profiles_pics')
    
    def __str__(self):
        return f"{ self.user.username } Profile"
    def save(self,*args ,**kwargs):
        super().save(*args ,**kwargs)
        
        if self.image:
            img = Image.open(self.image.path)
            
            if img.height > 1000 and img.width > 1000 and self.user.username :
                output_size  = (1000, 1000)
                img.thumbnail(output_size)
                img.save(self.image.path)
                
            
        