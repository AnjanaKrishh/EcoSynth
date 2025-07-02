from django.db import models

# Create your models here.

class uregistration(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()  # Add this
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_pic = models.FileField(upload_to='profile_pics/')

    def __str__(self):
        return self.name

