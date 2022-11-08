from django.db import models

from phone_field import PhoneField
from versatileimagefield.fields import VersatileImageField
from tinymce.models import HTMLField
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = models.EmailField(max_length=254)
    
    def __str__(self):
        return self.username
    
    
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
