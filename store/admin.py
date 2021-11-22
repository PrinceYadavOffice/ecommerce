from django.contrib import admin
from .models import Product, Customer, Order, CartItems, Shipping_Order

# Register your models here.
class ProductAdmin(admin.ModelAdmin):    
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product,ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(CartItems)
admin.site.register(Shipping_Order)