from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# class Customer(User):    
#     phone = models.CharField(max_length=10)   
#     address = models.TextField(max_length=250)
#     password1 = models.CharField(max_length=250)
#     password2 = models.CharField(max_length=250)


class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    image = models.ImageField(upload_to="products_img", null=True)
    total_units = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.name



