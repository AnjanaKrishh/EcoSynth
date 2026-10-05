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
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    message = models.TextField()
    rating = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.name}"

    

class SellProduct(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    image = models.FileField(upload_to='product_images/')
    address = models.TextField()
    phone = models.CharField(max_length=15)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device_name} by {self.user.name}"
    
    
class pmreg(models.Model):
    name = models.CharField(max_length=100, default='No Name')  # temporarily add default
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, default='')   # ✅ add default
    address = models.TextField(default='')                # ✅ add default
    password = models.CharField(max_length=100, default='default123')
    image = models.FileField(upload_to='images/')

class rmreg(models.Model):
    name = models.CharField(max_length=100, default='No Name')  # temporarily add default
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, default='')   # ✅ add default
    address = models.TextField(default='')                # ✅ add default
    password = models.CharField(max_length=100, default='default123')
    image = models.FileField(upload_to='images/')

    
class product(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.FileField(upload_to='media/',null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)


class PickupRequest(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=100)
    address = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    assigned_to = models.ForeignKey(pmreg, null=True, blank=True, on_delete=models.SET_NULL)
    points_assigned = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.name} - {self.waste_type} - {self.status}"
    
class RepairRequest(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    description = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    assigned_to = models.ForeignKey(rmreg, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
    
class DeliveryRequest(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    description = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')
    assigned_to = models.ForeignKey(rmreg, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Request by {self.user.name} for {self.device_type}"


class Cart(models.Model):
    user = models.ForeignKey(uregistration, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='In Cart')  # 'In Cart' or 'Ordered'

    def __str__(self):
        return f"{self.product.name} in {self.user.name}'s cart"
    
# filepath: c:\Users\Sagar\Documents\Project\Waste\EcoSynth\models.py
from django.db import models

class Blogs(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

