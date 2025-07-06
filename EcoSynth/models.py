from django.db import models

# Create your models here.

class uregistration(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()  # Add this
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=100,)
    profile_pic = models.FileField(upload_to='profile_pics/')

    def __str__(self):
        return self.name

class Feedback(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.name}"
    
from django.db import models
from .models import uregistration  # You already have this in the same file, so it's optional

class PickupRequest(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=100)
    address = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.name} - {self.waste_type} - {self.status}"


# models.py

class RepairRequest(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    description = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.name} - {self.device_type} - {self.status}"
    

class SellProduct(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    image = models.FileField(upload_to='product_images/')
    address = models.TextField()
    phone = models.CharField(max_length=15)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_name} by {self.user.name}"

 