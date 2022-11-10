from django.contrib import admin
from user.models import Customer, Login, Category, SubCategory, Product, MainBanner, SubBanners, HeaderFlash
 
# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(MainBanner)
admin.site.register(SubBanners)
admin.site.register(HeaderFlash)
admin.site.register(Login)