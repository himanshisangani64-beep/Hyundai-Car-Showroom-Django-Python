from django.urls import path
from . import views

urlpatterns = [
    path('product/', views.product_list_view, name='product'),
    path('product/<slug:category_slug>/', views.product_list_view, name='productcats'),
    path('pro_info/<int:product_id>/', views.pro_info, name='pro_info'),

]
