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
    name = models.CharField(max_length = 200) 
    price = models.IntegerField(default=0)

    category_choices = (
        ('Kids','Kids'),
        ('Mens','Mens'),
        ('Women','Women')
    )

    category = models.CharField(choices=category_choices, max_length = 5, default='none')
    description = models.CharField(max_length = 500, default="")
    image = models.ImageField(upload_to='product_images', default='')

    def __str__(self) -> str:
        return str(self.product_id) + ' ' + self.name