from django.contrib import admin
from App.models import Product, Order, Order_Item

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Order_Item)