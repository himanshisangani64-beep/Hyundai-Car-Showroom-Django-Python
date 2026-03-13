from django.urls import path
from . import views

urlpatterns = [
    path("bill/html/<int:order_id>/", views.view_bill, name="view_bill"),
    path("bill/pdf/<int:order_id>/", views.generate_bill, name="generate_bill"),

]

