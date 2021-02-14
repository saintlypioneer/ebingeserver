from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sku = models.CharField(unique=True, max_length=6)
    name = models.CharField(max_length=50)
    rating = models.IntegerField(default=4)
    cost_price = models.IntegerField(null=False)
    selling_price = models.IntegerField()
    image = models.ImageField(null=False, upload_to='static/assets/app1')
    image2 = models.ImageField(null=True, upload_to='static/assets/app1')
    image3 = models.ImageField(null=True, upload_to='static/assets/app1')
    qty_available = models.IntegerField(default=1)
    unit = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=20, blank=True)
    sub_category = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=200, null=False)
    brief_description = models.CharField(max_length=30, blank=True)
    tags = models.CharField(max_length=200, blank=True, null=True)
    color = models.CharField(max_length=20)
class Client(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    detail = models.OneToOneField(User, on_delete=models.CASCADE)
    mob = models.CharField(max_length=12)
    add1 = models.CharField(max_length=30)
    add2 = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=20)
    cart = models.CharField(max_length=5000)
    wishlist = models.CharField(max_length=2000)
class Order(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    mob = models.CharField(max_length=12)
    add1 = models.CharField(max_length=30)
    add2 = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=20)
    date = models.DateField(auto_now=True)
    # status = models.IntegerField(default=)
    # status = 1:created, 0:delivered, -1:cancelled, 
class OrderedProducts(models.Model):
    selling_price = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)