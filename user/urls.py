from django.urls import path,include
from . import views

app_name = "user"

urlpatterns = [
    path("about-us", views.about_us, name="about_us"),
    path("blog-detail", views.blog_detail, name="blog_detail"),
    path("blog-grid", views.blog_grid, name="blog_grid"),
    path("blog-list", views.blog_list, name="blog_list"),
    path("cart", views.cart, name="cart"),
    path("checkout", views.checkout, name="checkout"),
    path("coming-soon", views.coming_soon, name="coming_soon"),
    path("compare", views.compare, name="compare"),
    path("contact-us", views.contact_us, name="contact_us"),
    path("faq", views.faq, name="faq"),
    path("forgot", views.forgot, name="forgot"),
    path("index-2", views.index_2, name="index_2"),
    path("index-3", views.index_3, name="index_3"),
    path("index-4", views.index_4, name="index_4"),
    path("index-5", views.index_5, name="index_5"),
    path("index-6", views.index_6, name="index_6"),
    path("index-7", views.index_7, name="index_7"),
    path("index-8", views.index_8, name="index_8"),
    path("index-9", views.index_9, name="index_9"),
    path("", views.index, name="index"),
    path("login", views.login_views, name="login"),
    path("order-success", views.order_success, name="order_success"),
    path("order-tracking", views.order_tracking, name="order_tracking"),
    path("otp", views.otp, name="otp"),
    path("product-4-image", views.product_4_image, name="product_4_image"),
    path("product-bottom-thumbnail", views.product_bottom_thumbnail, name="product_bottom_thumbnail"),
    path("product-bundle", views.product_bundle, name="product_bundle"),
    path("product-left-thumbnail", views.product_left_thumbnail, name="product_left_thumbnail"),
    path("product-right-thumbnail", views.product_right_thumbnail, name="product_right_thumbnail"),
    path("product/<int:id>", views.product, name="product"),
    path("product-sticky", views.product_sticky, name="product_sticky"),
    path("search", views.search, name="search"),
    path("seller-become", views.seller_become, name="seller_become"),
    path("seller-dashboard", views.seller_dashboard, name="seller_dashboard"),
    path("seller-detail-2", views.seller_detail_2, name="seller_detail_2"),
    path("seller-detail", views.seller_detail, name="seller_detail"),
    path("seller-grid-2", views.seller_grid_2, name="seller_grid_2"),
    path("seller-grid", views.seller_grid, name="seller_grid"),
    path("shop-banner", views.shop_banner, name="shop_banner"),
    path("shop-category-slider", views.shop_category_slider, name="shop_category_slider"),
    path("shop-category", views.shop_category, name="shop_category"),
    path("shop/<int:id>", views.shop, name="shop"),
    path("shop-list", views.shop_list, name="shop_list"),
    path("shop-right-sidebar", views.shop_right_sidebar, name="shop_right_sidebar"),
    path("shop-top-filter", views.shop_top_filter, name="shop_top_filter"),
    path("sign-up", views.user_register, name="sign_up"),
    path("user-dashboard", views.user_dashboard, name="dashboard"),
    path("wishlist/<int:id>", views.wishlist, name="wishlist"),
    path("404", views.error_404, name="error_404"),
    
]
