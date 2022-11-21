from user.models import Category
from user.models import SubCategory
from user.models import Product
from user.models import HeaderFlash
from user.models import Customer

def main_context(request):
    headerflash = HeaderFlash.objects.last()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    products = Product.objects.all()
    user = request.user
    print(user)
    
    if Customer.user == request.user:
       
        return {
            "headerflash": headerflash,
            "categories": categories,
            "subcategories": subcategories,
            "products": products,
            "status":1
            }
    else:
       
        return {
            "headerflash": headerflash,
            "categories": categories,
            "subcategories": subcategories,
            "products": products,
            "status":0
            }
