from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    current_city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'



    #def save(self, *args, **kwargs): 
        #super().save(*args, **kwargs)  

        #img = Image.open(self.image.path)

        #if img.height > 300 or img.width > 300:
           # output_size = (300, 300)
            #img.thumbnail(output_size)
            #img.save(self.image.path)
