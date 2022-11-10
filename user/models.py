from django.db import models
from versatileimagefield.fields import VersatileImageField
from tinymce.models import HTMLField

from django.contrib.auth.models import (
    AbstractUser,
 )

# Create your models here.


# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):

#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         if user:
#             return user

#     def create_superuser(self, username, password=None, **extra_fields):

#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save(using=self._db)
#         return user

class Login(AbstractUser):
    is_customer = models.BooleanField(default=False)
    

class Customer(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='user')
    customer_name = models.CharField(max_length = 100,null=True)
    phone_number = models.CharField(default=0, null=True, max_length=10, unique = True)  
    email = models.EmailField(max_length=254,null=True)
    address = models.CharField(max_length = 250)
    
   



# class Customer(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
#     customer_name = models.CharField(max_length = 100,null=True)
#     phone_number = models.CharField(max_length=50,blank=True,null=True)
#     email = models.EmailField(max_length=254,null=True)
#     address = models.CharField(max_length = 250)
#     username = models.CharField(max_length=100,null=True)
    

    # def __str__(self):
    #     return self.customer_name
    
    
class Category(models.Model):
    category = models.CharField(max_length = 200)
    image = VersatileImageField(upload_to="categories/", null=True)
     
    def __str__(self):
        return self.category
    
    
class SubCategory(models.Model):
    subcategory = models.CharField(max_length = 150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory
    
    
class Product(models.Model):
    product = models.CharField(max_length = 150)
    image = VersatileImageField(upload_to="products/", null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.IntegerField()
    offer_price = models.IntegerField(null = True)
    description = HTMLField()
    is_top_save_today= models.BooleanField(default = False)
    is_best_seller = models.BooleanField(default = False)
        
    def __str__(self):
        return self.product
    

class MainBanner(models.Model):
    bannerbig = VersatileImageField(upload_to="MainBanner/", null=True)
        
    def __str__(self):
        return self.bannerbig


class SubBanners(models.Model):
    sub_banner1 = VersatileImageField(upload_to="SubBanners/", null=True)
    sub_banner2 = VersatileImageField(upload_to="SubBanners/", null=True)

    def __str__(self):
        return self.sub_banner1
    

class HeaderFlash(models.Model):
    address =  HTMLField()
    offer_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.address
    
        
def get_absolute_url(self):
    return reverse("_detail", kwargs={"pk": self.pk})
