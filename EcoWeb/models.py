from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import CustomUserManager

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    otp = models.IntegerField(null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username","password"]

    objects = CustomUserManager()

    def __str__(self):
        return str(self.email)


class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    sequence = models.IntegerField(default=100)

    def __str__(self):
        return str(self.name)




class Product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.PROTECT,default=1)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    unit = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    sequence = models.IntegerField(default=100)

    def __str__(self):
        return str(self.name)



class Order(models.Model):
    STATUS_CHOICES = [
        (1, 'on_delivery'),
        (2, 'delivered'),
    ]

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    date = models.DateField(auto_now=True)
    total = models.FloatField(default=0)
    status = models.IntegerField(choices=STATUS_CHOICES)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class OrderDetail(models.Model):
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null = True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    qty = models.IntegerField(default=0,null=True)
    price = models.FloatField()

    def __str__(self):
        return str(self.id)



