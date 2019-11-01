from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Manger for user profile"""

    def create_user(self, email, name, password = None):
        """Create a new User profile"""
        if not email:
            raise ValueError('user must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password=None):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """ Retrieve full name of user"""
        return self.name
    
    def def_short_name(self):
        """Retrieve short name of user"""
        return self.name
    
    def __str__(self):
        """Return string representation of our user"""
        return self.email
    
class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status_text = models.CharField(max_length=255, default='DEFAULT VALUE')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return the model as string"""
        return self.status_text

class ProductCategory(models.Model):

    """Product Category"""
    product_category = models.CharField(max_length=255, default='DEFAULT VALUE')

    def __str__(self):
        return self.product_category

class ProductList(models.Model):

    """Profile status update"""
    product_category = models.ForeignKey(
        'profiles_api.ProductCategory',
        on_delete=models.CASCADE,
    )

    product_name = models.CharField(max_length=255, default='DEFAULT VALUE')
    product_img_field = models.ImageField(upload_to='media', max_length=254)
    product_price = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """return the model as string"""
        return self.product_name