from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Product_Type(models.TextChoices):
    kurti = 'Kurti'
    trousers = 'Trousers'

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    product_image = models.FileField(upload_to='images/', null=True, verbose_name="")
    product_type = models.CharField(max_length=200, choices=Product_Type.choices, default=Product_Type.choices[0])
    price = models.IntegerField()
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(product_id__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

class Order_Item(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


