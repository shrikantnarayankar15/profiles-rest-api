from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
# Create your models here.

class ProductList(models.Model):
    """Profile status update"""
    product_name = models.CharField(max_length=255)
    product_img_field = models.ImageField(upload_to='media', max_length=254)
    product_price = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return the model as string"""
        return self.product_name