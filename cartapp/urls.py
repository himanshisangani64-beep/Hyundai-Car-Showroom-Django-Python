# cartapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('addtocart/', views.addtocart, name='addtocart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),

    # login/registration routes
    path('registration1/', views.registration1, name='registration1'),
    path('regidata1/', views.regidata1, name='regidata1'),
    path('login1/', views.login1, name='login1'),
    path('logincheck1/', views.logincheck1, name='logincheck1'),
    path('pro_info1/', views.pro_info1, name='pro_info1'),
]
