from django.urls import path
from . import views

urlpatterns = [
    path("place_order1/", views.place_order1, name="place_order1"),
    path("order/success/<int:order_id>/", views.order_success, name="order_success"),
    path('order/remove-item/<int:order_id>/<int:product_id>/', views.remove_order_item, name='remove_order_item'),

]
