from email.policy import default
from random import choices
from secrets import choice
from statistics import mode
from tkinter.tix import INCREASING
from unicodedata import category
from unittest.util import _MAX_LENGTH
from xml.parsers.expat import model
from django.db import models

# Create your models here.
class Products(models.Model):
    product_id  = models.AutoField(primary_key = True)
    listedBy = models.IntegerField(default=0)
    name = models.CharField(max_length = 200) 
    price = models.IntegerField(default=0)

    category_choices = (
        ('Kids','Kids'),
        ('Mens','Mens'),
        ('Women','Women')
    )

    category = models.CharField(choices=category_choices, max_length = 5, default='none')

    sub_category = (
        ('Summer', 'Summer'),
        ('Winter', 'Winter')
    )

    sub_category = models.CharField(choices=sub_category, default='none', max_length=10)

    description = models.CharField(max_length = 500, default="")
    image = models.ImageField(upload_to='product_images', default='')

    def __str__(self) -> str:
        return str(self.product_id) + ' ' + self.name
    

class Trial(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return self.name + str(self.quantity)  
    

class Seller(models.Model):
    Id = models.AutoField(primary_key=True, unique=True, default=1001)
    name = models.CharField(max_length=200)
    Mobile = models.IntegerField()
    ShopName = models.CharField(max_length=200)
    VerificationDocument = models.ImageField(upload_to='seller_documents', default='')

    verfication_choices = (
        ('Verified', 'Verified'),
        ('Not Verified', 'Not Verified')
    )

    VerificationStatus = models.CharField(choices=verfication_choices, default='Not Verified',max_length=50)

    def __str__(self) -> str:
        return str(self.Id) + '-' + self.ShopName + '-' + self.VerificationStatus 
    

class PaymentDetails(models.Model):
    Seller_id = models.IntegerField()
    Customer_id = models.IntegerField()
    Order_id = models.CharField(max_length=200)
    Payment_id = models.CharField(max_length=200)
    Signature = models.CharField(max_length=200)
    Amount = models.IntegerField()

    status_choices = (
        ('Success', 'Success'),
        ('Failed', 'Failed')
    )

    Status = models.CharField(choices=status_choices, default='Failed', max_length=50)

    def __str__(self) -> str:
        return self.Order_id + '-->' + self.Status
    

class Cart(models.Model):
    user_id = models.IntegerField()
    prod_id = models.IntegerField()
    listedBy = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    image = models.ImageField(upload_to='product_images', default='')
    title = models.CharField(max_length=200,default='')
    desc = models.CharField(max_length=200,default='')
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return "UserId: " + str(self.user_id) + " ProductId: " + str(self.prod_id)