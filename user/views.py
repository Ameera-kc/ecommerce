from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginRegister, UserRegistration
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from user.models import MainBanner, Product, SubCategory, Category, SubBanners1, SubBanners2,Wishlist, Customer, AddToCart, ChangePassword, Order, CashonDeliveyOrders
from user.models import Coupon, CouponUsed, NoStock, OrderTracking, Rating, CustomerProductRating
from django.contrib.auth.decorators import login_required
from .helper import send_forget_password_mail
import uuid
from django.contrib.auth import logout
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Sum
import datetime
import razorpay
from ecom.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
# from django.http.response import JsonResponse

# Create your views here.

razorpay_client = razorpay.Client(
    auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))


def logout_view(request):
    logout(request)
    return redirect('user:login')

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
    if request.method == "POST":
        login_form = LoginRegister(request.POST)
        user_form = UserRegistration(request.POST)
        if login_form.is_valid() and user_form.is_valid():
            user = login_form.save(commit=False)
            user.is_customer = True
            user.save()
            c = user_form.save(commit=False)
            c.user = user
            c.save()
            messages.info(request, 'User Registration Successfull')
            return redirect('user:login')
    return render(request, 'web/sign-up.html', {'login_form': login_form, 'user_form': user_form})

def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_obj = Customer.objects.get(email=email)
        token = str(uuid.uuid4())
        ChangePassword.objects.create(user=user_obj,forgot_password_token=token)
        send_forget_password_mail(user_obj.email,token)
        messages.warning(request, "An email is sent")
        return redirect("user:forgot password")
    context = {}
    return render(request, "web/forgot.html", context)

def change_password(request,token):
    change_password_obj = ChangePassword.objects.get(forgot_password_token=token)
    if change_password_obj.status == True:
        messages.error(request, "Link expired...")
        return redirect('web:forget password')
    if change_password_obj.user:
        customer = Customer.objects.all()
        for customer in customer:
            if change_password_obj.user == customer:
                if change_password_obj.user.email == customer.email:
                    user_id=Customer.objects.filter(email=change_password_obj.user.email).first()
                context = {'manager_id':change_password_obj.user.id}
                return render(request,'web/change-password.html',context)

def index(request):
    mainbanner = MainBanner.objects.last()
    subbanners1 = SubBanners1.objects.last()
    subbanners2 = SubBanners2.objects.last()
    topsave = Product.objects.filter(is_top_save_today = True)
    bestseller = Product.objects.filter(is_best_seller = True)
    # a=bestseller-3
    # b=bestseller-6
    # bestseller1 = Product.objects.filter(is_best_seller = True)[4:2:-1]
    # bestseller2 = Product.objects.filter(is_best_seller = True)[2:0:-1]
    context = {
        "mainbanner":mainbanner,
        "subbanner1":subbanners1,
        "subbanner2":subbanners2,
        "topsave":topsave,
        # "bestseller1":bestseller1,
        # "bestseller2":bestseller2,
        "bestseller":bestseller
    }
    return render(request, "web/index.html", context)

def product(request, id):
    products = Product.objects.get(id=id)
    sub = products.subcategory
    if products.offer_price:
        percentage=((products.price-products.offer_price)/products.price)*100
    else:
        percentage=None
    if Rating.objects.filter(product__product=products):
        stars_obj=Rating.objects.get(product__product=products)
        stars=int(stars_obj.rating)
        nostar=5-stars
        print("nostar",nostar)
        print("type of nostar",type(nostar))
        context = {
            "products": products,
            "subcategory": sub,
            "percentage":percentage,
            "stars":stars,
            "nostar":nostar
            }
    else:
        context = {
            "products": products,
            "subcategory": sub,
            "percentage":percentage
            }
    return render(request, "web/product-slider.html", context)

        
def shop(request,id):
    category = Category.objects.get(id=id)
    
    context = {
        "category":category,
    }
    return render(request, "web/shop-left-sidebar.html", context)

def shop_category(request,id):
    subcategory = SubCategory.objects.filter(id=id)
    context = {
        "subcategory":subcategory
    }
    return render(request, "web/shop-category.html", context)

# @csrf_protect
# @login_required(login_url='login')

def addtowishlist(request,id):
        
        if request.user.is_authenticated:
            if Customer.objects.get(user = request.user):
                print(request.user)
                product = Product.objects.get(id=id)  
                if product:
                    cust = Customer.objects.get(user=request.user)
                    if Wishlist.objects.filter(user=cust,product=product):
                    
                        messages.warning(request, "product is already in wishlist...")
                        return redirect('/') 
                    else:
                        user = Customer.objects.get(user=request.user)
                        Wishlist.objects.create(user=user,product=product)
                        messages.warning(request, "Product added successfully...")   
                        return redirect('/') 
                    # return JsonResponse({'status':"Product added successfully"}) 
                else:
                
                    messages.error(request, "No such product found...") 
                
            else:
            
                messages.error(request, "Login to continue")
                return redirect('user:login')
        else:
            
            messages.error(request, "Login to continue")
            return redirect('user:login')
            
def viewwishlist(request):
    if request.user.is_authenticated:
        if Customer.objects.get(user = request.user):
            my_p = Customer.objects.get(user=request.user)
            wished_item = Wishlist.objects.filter(user=my_p)
            context= {
            'wished_items':wished_item
            }
            return render(request,'web/wishlist.html',context)  
        else:
            messages.error(request,"pls login to continue")
            return redirect('user:login')
    else:
            messages.error(request,"pls login to continue")
            return redirect('user:login')

def deletefromwishlist(request,id): 
                    user = Customer.objects.get(user=request.user)                              
                    product = Wishlist.objects.get(user=user,id=id)   
                    product.delete()
                    messages.warning(request, "Product removed successfully...") 
                    return redirect('/')   
                    # return JsonResponse({'status':"Product added successfully"})              
def addtocart(request,id):
    if request.user.is_authenticated:
        if Customer.objects.get(user = request.user):
            product = Product.objects.get(id=id)
            price = product.price
            if product:
                my_p = Customer.objects.get(user=request.user)
                if AddToCart.objects.filter(user=my_p,product=product):
                    messages.warning(request,"product is already in cart")
                    return redirect('/') 
                else:  
                    my_p = Customer.objects.get(user=request.user)
                    AddToCart.objects.create(user=my_p,product=product,total=price) 
                    messages.warning(request,"Product added successfully")    
                    return redirect('/') 
            else:
                messages.error(request,"product is not available")
                return redirect('/') 
        else:
            messages.warning(request,"Login to Continue")
            return redirect('user:login')
    else:
            messages.warning(request,"Login to Continue")
            return redirect('user:login')

def addQuantity(request):
        quantity = request.GET['quantity']
        my_p = Customer.objects.get(user=request.user)
        id = request.GET['id']
        cart_obj = AddToCart.objects.get(id=id,user=my_p)
        new_quantity = int(quantity) +1 
        product_total = float(new_quantity) * float(cart_obj.product.offer_price)
        cart_obj.total = product_total
        cart_obj.save()
        AddToCart.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
        data = {
            'total':cart_obj.total,
        }
        return JsonResponse(data)

def lessQuantity(request):
    quantity = request.GET['quantity']
    my_p = Customer.objects.get(user=request.user)
    id = request.GET['id']
    cart_obj = AddToCart.objects.get(id=id,user=my_p)
    new_quantity = int(quantity) - 1
    product_total = float(new_quantity) * float(cart_obj.product.offer_price)
    cart_obj.total = product_total
    cart_obj.save()
    AddToCart.objects.filter(id=id).update(quantity=new_quantity, total=product_total)
    data = {
        'total':cart_obj.total,
    }
    return JsonResponse(data) 
    
@csrf_exempt
def viewcart(request):
    if request.user.is_authenticated:
        if request.user:
            print(request.user)
            # if request.method == 'POST':
            #     coupon = request.POST.get('coupon')
            #     coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
            #     if not coupon_obj.exists():
            #         messages.warning(request,'Invalid Coupon')
            #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
            #     if cart_obj.coupon:
            #         messages.warning(request,'Coupon already exists')
            #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
            #     if cart_obj.get_cart_total()>coupon_obj[0].minimum_amount[0]:
            #         messages.warning(request,'Amount should be greater than {coupon_obj.minimum_amount}')
            #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                
            #     if coupon_obj[0].is_expired[0]:
            #         messages.warning(request,'coupon expired')
            #         return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
                    
            #     cart_obj.coupon=coupon_obj[0]
            #     cart_obj.save()
            #     messages.warning(request,'Coupon applied')
            #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
               
            my_p = Customer.objects.get(user=request.user)
            sub_total = AddToCart.objects.filter(user__user=(request.user)).aggregate(Sum('total'))
            carted_item = AddToCart.objects.filter(user=my_p)
            context= {
                'carted_item':carted_item,
                'sub_total':sub_total,
            }
            return render(request,'web/cart.html',context)        
        else:
            messages.warning(request,"Login to Continue")
            return redirect('user:login')
    else:
            messages.warning(request,"Login to Continue")
            return redirect('user:login')  

def deletefromcart(request,id):                
                    user = Customer.objects.get(user=request.user)                              
                    product = AddToCart.objects.get(user=user,id=id)   
                    product.delete()
                    messages.warning(request, "Product removed successfully...") 
                    return redirect('/')   
                
def checkout(request):
    if request.user.is_authenticated:
        if Customer.objects.get(user = request.user):
            my_p = Customer.objects.get(user=request.user)
            carted_item = AddToCart.objects.filter(user=my_p)
            # sub_total = AddToCart.objects.filter(user__user=(request.user)).aggregate(Sum('total'))
            if CouponUsed.objects.filter(user = my_p):
                
                print("coupon")
                sub_total = AddToCart.objects.filter(user__user=(request.user)).aggregate(Sum('total'))
                coupon = CouponUsed.objects.filter(user = my_p).last()
                print("hi")
                print(coupon)
                print("hlo")
                if coupon.used_time == 1:
                    print("used_time",coupon.used_time)
                    c_amount = 0
                else:
                    print(coupon)
                    c = coupon.coupon_code
                    c_amount = c.discount_price
                    print(c_amount)
                sub_total = sub_total['total__sum']
                total = sub_total - c_amount
                print(total)
                context= {
                        'carted_item':carted_item,
                        'sub_total':total,
                }
                return render(request,'web/checkout.html',context)
            else:
                print("no coupon")
                sub_total = AddToCart.objects.filter(user__user=(request.user)).aggregate(Sum('total'))
                context= {
                    'carted_item':carted_item,
                    'sub_total':sub_total,
                }
                return render(request,'web/checkout.html',context)  
        else:
            messages.warning(request,"Login to Continue")
            return redirect('user:login')
    else:
            messages.warning(request,"Login to Continue")
            return redirect('user:login') 

# coupon 
def couponApplied(request):
    code=request.GET.get("code")
    customer = Customer.objects.get(user=request.user)
   
    if Coupon.objects.filter(coupon_code = code):
        exist = CouponUsed.objects.filter(coupon_code__coupon_code = code, user = customer).exists()
        if exist:
            coupon = CouponUsed.objects.get(coupon_code__coupon_code = code, user = customer)
            print(coupon.user)
            print(coupon.used_time)
            if coupon.used_time == 1:
                messages.error(request,'coupon is used once')
                return redirect('user:viewcart') 
        else:
            code_obj = Coupon.objects.get(coupon_code=code)
            if code_obj.is_expired:
                messages.error(request,'coupon expired')
                return redirect('user:viewcart')
            else:
                numberofused = 1
                CouponUsed.objects.create(user = customer, coupon_code = code_obj, used_time = numberofused)
                messages.warning(request,'coupon is applied')
                return redirect('user:viewcart')
    else:
        messages.error(request,"Coupon doesn't exist")
        return redirect('user:viewcart')
    
# payment
from .constants import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
import json

def order_payment(request):
    my_p = Customer.objects.get(user=request.user)
    carted_item = AddToCart.objects.filter(user=my_p)
    for item in carted_item:
        productobj = Product.objects.get(product = item)
        productobj.quantity=productobj.quantity-item.quantity
        Product.objects.filter(product = item).update(quantity=productobj.quantity)
        if productobj.quantity <= 3:
            nostock = NoStock.objects.create(product=productobj)
            nostock.save()
    
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        email = request.POST.get("email")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        landmark = request.POST.get("landmark")
        date = datetime.datetime.now().strftime("%Y-%d-%m %H:%M:%S")
        print(date,"date")
        client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            order_date=str(date) ,name=name, amount=amount, email=email, address=address, contact=contact, landmark=landmark, provider_order_id=razorpay_order["id"]
        )
        order.save()
        print(order.order_date,"order.order_date")
        return render(
            request,
            "web/payment.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/order_success/",
                "razorpay_key": RAZORPAY_API_KEY,
                "order": order,
            },
        )
    return render(request, "request,'web/checkout.html',context")

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))
        return client.utility.verify_payment_signature(response_data)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.provider_order_id = order.provider_order_id
            order.save()
            return render(request, "web/order-success.html", context={"status": order.status,"order_id":order.provider_order_id})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "web/order-success.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "web/order-success.html", context={"status": order.status})


def order_success2(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        landmark = request.POST.get("landmark")
        date = datetime.datetime.now()
        print(date,"date")
        order = CashonDeliveyOrders.objects.create(
            order_date=date, name=name, amount=amount, address=address, contact=contact, email=email, landmark=landmark
        )
        order.save()
        print(order.order_date,"order.order_date")
        return render(
            request,
            "web/order-success.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "/order_success/",
                "razorpay_key": RAZORPAY_API_KEY,
                "order": order,
            },
        )
    return render(request,'web/order-success.html')
    
def about_us(request):
    context = {}
    return render(request, "web/about-us.html", context)

def coming_soon(request):
    context = {}
    return render(request, "web/coming-soon.html", context)

def contact_us(request):
    context = {}
    return render(request, "web/contact-us.html", context)

def order_tracking(request):
    my_p = Customer.objects.get(user=request.user) 
    ordertracking = OrderTracking.objects.filter(user=my_p)
    kw=request.GET.get("search")
    if kw:
        if (Order.objects.filter(Q(provider_order_id__icontains=kw))):
            results = Order.objects.filter(Q(provider_order_id__icontains=kw))
            print(kw)
            print(results)
            for i in ordertracking.values():
                orderPlaced = (i['orderPlaced'])
                orderPlacedtime = (i['orderPlacedtime'])
                preparingToShip = (i['preparingToShip'])
                preparingToShiptime = (i['preparingToShiptime'])
                Shipped = (i['Shipped'])
                ShippedTime = (i['ShippedTime'])
                Delivered = (i['Delivered'])
                DeliveredDateAndTime = (i['DeliveredDateAndTime'])
                context = {
                "orderPlaced":orderPlaced,
                "orderPlacedtime":orderPlacedtime,
                "preparingToShip":preparingToShip,
                "preparingToShiptime":preparingToShiptime,
                "Shipped":Shipped,
                "ShippedTime":ShippedTime,
                "Delivered":Delivered,
                "DeliveredDateAndTime":DeliveredDateAndTime,
                "results" : results,
                "status" : 1,
                }
                
                return render(request, "web/order-tracking.html", context) 
            return render(request, "web/order-tracking.html", context) 
        else: 
            messages.error(request, "No matching products found...") 
            context = {
            "status":0
            }
            return render(request, "web/order-tracking.html", context) 
    else:
        return render(request, "web/order-tracking.html")
    
    
    
def search(request):
    kw=request.GET.get("search")
    if kw:
        if (Product.objects.filter(Q(product__icontains=kw) or Q(description__icontains=kw))):
            results = Product.objects.filter(Q(product__icontains=kw) | Q(description__icontains=kw))
            print(kw)
            print(results)
            context = {
            "results" : results,
            "status":1
            }
            return render(request, "web/search.html", context) 
        else: 
            messages.error(request, "No matching products found...") 
            context = {
            "status":0
            }
            return render(request, "web/search.html", context) 
    else:
        return render(request, "web/search.html")

def seller_dashboard(request):
    context = {}
    return render(request, "web/seller-dashboard.html", context)

def sign_up(request):
    context = {}
    return render(request, "web/sign-up.html", context)

def user_dashboard(request):
    context = {}
    return render(request, "web/user-dashboard.html", context)

def error_404(request):
    context = {}
    return render(request, "web/404.html", context)

def productrating(request,id):
    # user=Customer.objects.get(user = request.user)
    user = request.GET.get("name")
    code = int(request.GET.get("rg1"))
    email=request.GET.get("email")
    name=Product.objects.get(id=id)
    if code == 5:
        customrating=CustomerProductRating.objects.create(user=user,product=name,rating=1,email=email)
        customrating.save()
    elif code == 4:
        customrating=CustomerProductRating.objects.create(user=user,product=name,rating=2,email=email)
        customrating.save()
    elif code == 3:
        customrating=CustomerProductRating.objects.create(user=user,product=name,rating=3,email=email)
        customrating.save()
    elif code == 2:
        customrating=CustomerProductRating.objects.create(user=user,product=name,rating=4,email=email)
        customrating.save()
    elif code == 1:
        customrating=CustomerProductRating.objects.create(user=user,product=name,rating=5,email=email)
        customrating.save()
    else:
        star=int(0)
        customrating=CustomerProductRating.objects.create(user=user,product=name,rating=star,email=email)
        customrating.save()
    rates=CustomerProductRating.objects.filter(product=name).aggregate(Sum('rating'))
    print("rates",rates)
    rate = rates['rating__sum']
    print("rrrrrrrrrrrrrr")
    print("rate",rate)
    if rate == None:
        rate=0
    count=CustomerProductRating.objects.filter(product=name).count()
    print(type(count),"type")
    if count == 0:
        if Rating.objects.create(product=name):
            rating=Rating.objects.update(product=name,rating=rate)
            rating.save()
        else:
            rating=Rating.objects.create(product=name,rating=rate)
            rating.save()
        return redirect('user:product',id)
    else:
        c=count*5
        print("c",c)
        rates=c/rates
        print("rates",rates)
        rates=rates*10
        print("rates",rates)
        if Rating.objects.filter(product__product=name):
            Rating.objects.filter(product=name).update(rating=rates)
        else:
            rating=Rating.objects.create(product=name,rating=rates)
            rating.save()
        return redirect('user:product',id)
    
   
    