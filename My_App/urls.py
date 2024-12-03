from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart_page_cookie, name='cart_page'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist_cookie, name='add_to_wishlist'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart_cookie, name='remove_from_cart_cookie'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist_cookie, name='remove_from_wishlist_cookie'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_cookie, name='add_to_cart_cookie'),
    path('wishlist/', views.wishlist_page_cookie, name='wishlist_page_cookie'),
    path('buy/<int:product_id>/', views.buy_page, name='buy_page'),
    path('purchase-success/<int:order_id>/', views.purchase_success, name='purchase_success'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('contact/', views.contact_page, name='contact'),
    
]