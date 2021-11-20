from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):    
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)   
    address = models.TextField(max_length=250)

    def __str__(self):
        return str(self.user)
        

class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    image = models.ImageField(upload_to="products_img", null=True)
    slug = models.SlugField(unique=True, db_index=True)
    total_units = models.IntegerField()
    description = models.TextField(max_length=400, null=True)    
    price = models.FloatField()

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.get_total for item in cartitems])
        return total  
    
    @property
    def get_items_total(self):
        cartitems = self.cartitems_set.all()
        total = sum([item.quantity for item in cartitems])
        return total     


class CartItems(models.Model):    
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    def __str__(self):
        return str(self.id)
    


