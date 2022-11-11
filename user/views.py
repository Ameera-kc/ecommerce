from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginRegister, UserRegistration
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
@csrf_exempt
def login_views(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_customer:
                return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
    return render(request, 'web/login.html')

@csrf_exempt
def user_register(request):
    login_form = LoginRegister()
    user_form = UserRegistration()
    print("hi")
    if request.method == "POST":
        login_form = LoginRegister(request.POST)
        print(login_form)
        user_form = UserRegistration(request.POST)
        print(user_form)
        print("hlo")
        if login_form.is_valid() and user_form.is_valid():
            print("valid")
            user = login_form.save(commit=False)
            user.is_user = True
            user.save()
            print("hloo")
            c = user_form.save(commit=False)
            c.user = user
            c.save()
            print("hloo")
            messages.info(request, 'User Registration Successfully')
            return redirect('user:login')
    return render(request, 'web/sign-up.html', {'login_form': login_form, 'user_form': user_form})


def index(request):
    context = {}
    return render(request, "web/index.html", context)




def about_us(request):
    context = {}
    return render(request, "web/about-us.html", context)


def blog_detail(request):
    context = {}
    return render(request, "web/blog-detail.html", context)


def blog_grid(request):
    context = {}
    return render(request, "web/blog-grid.html", context)


def blog_list(request):
    context = {}
    return render(request, "web/blog-list.html", context)


def cart(request):
    context = {}
    return render(request, "web/cart.html", context)


def checkout(request):
    context = {}
    return render(request, "web/checkout.html", context)


def coming_soon(request):
    context = {}
    return render(request, "web/coming-soon.html", context)


def compare(request):
    context = {}
    return render(request, "web/compare.html", context)


def contact_us(request):
    context = {}
    return render(request, "web/contact-us.html", context)


def faq(request):
    context = {}
    return render(request, "web/faq.html", context)


def forgot(request):
    context = {}
    return render(request, "web/forgot.html", context)


def index_2(request):
    context = {}
    return render(request, "web/index-2.html", context)


def index_3(request):
    context = {}
    return render(request, "web/index-3.html", context)


def index_4(request):
    context = {}
    return render(request, "web/index-4.html", context)


def index_5(request):
    context = {}
    return render(request, "web/index-5.html", context)


def index_6(request):
    context = {}
    return render(request, "web/index-6.html", context)


def index_7(request):
    context = {}
    return render(request, "web/index-7.html", context)


def index_8(request):
    context = {}
    return render(request, "web/index-8.html", context)


def index_9(request):
    context = {}
    return render(request, "web/index-9.html", context)





def order_success(request):
    context = {}
    return render(request, "web/order-success.html", context)


def order_tracking(request):
    context = {}
    return render(request, "web/order-tracking.html", context)


def otp(request):
    context = {}
    return render(request, "web/otp.html", context)


def product_4_image(request):
    context = {}
    return render(request, "web/product-4-image.html", context)


def product_bottom_thumbnail(request):
    context = {}
    return render(request, "web/product-bottom-thumbnail.html", context)


def product_bundle(request):
    context = {}
    return render(request, "web/product-bundle.html", context)


def product_left_thumbnail(request):
    context = {}
    return render(request, "web/product-left-thumbnail.html", context)


def product_right_thumbnail(request):
    context = {}
    return render(request, "web/product-right-thumbnail.html", context)


def product_slider(request):
    context = {}
    return render(request, "web/product-slider.html", context)


def product_sticky(request):
    context = {}
    return render(request, "web/product-sticky.html", context)


def search(request):
    context = {}
    return render(request, "web/search.html", context)


def seller_become(request):
    context = {}
    return render(request, "web/seller-become.html", context)


def seller_dashboard(request):
    context = {}
    return render(request, "web/seller-dashboard.html", context)


def seller_detail_2(request):
    context = {}
    return render(request, "web/seller-detail-2.html", context)


def seller_detail(request):
    context = {}
    return render(request, "web/seller-detail.html", context)


def seller_grid_2(request):
    context = {}
    return render(request, "web/seller-grid-2.html", context)


def seller_grid(request):
    context = {}
    return render(request, "web/seller-grid.html", context)


def shop_banner(request):
    context = {}
    return render(request, "web/shop-banner.html", context)


def shop_category_slider(request):
    context = {}
    return render(request, "web/shop-category-slider.html", context)


def shop_category(request):
    context = {}
    return render(request, "web/shop-category.html", context)


def shop(request):
    context = {}
    return render(request, "web/shop-left-sidebar.html", context)


def shop_list(request):
    context = {}
    return render(request, "web/shop-list.html", context)


def shop_right_sidebar(request):
    context = {}
    return render(request, "web/shop-right-sidebar.html", context)


def shop_top_filter(request):
    context = {}
    return render(request, "web/shop-top-filter.html", context)


def sign_up(request):
    context = {}
    return render(request, "web/sign-up.html", context)


def user_dashboard(request):
    context = {}
    return render(request, "web/user-dashboard.html", context)


def wishlist(request):
    context = {}
    return render(request, "web/wishlist.html", context)


def error_404(request):
    context = {}
    return render(request, "web/404.html", context)

