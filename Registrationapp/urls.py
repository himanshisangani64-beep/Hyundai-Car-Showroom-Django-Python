from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # ✅ Import added

urlpatterns = [
    path('', views.home, name='home'),
    #path('logout/', views.custom_logout, name='logout'),
    path('logout1/', views.logout_view, name='logout1'),
    path('registration/', views.registration, name='registration'),
    path('regidata/', views.regidata, name='regidata'),
    path('login/', views.login, name='login'),
    path('logincheck/', views.logincheck, name='logincheck'),
    path('dashboard/', views.dashboard, name='dashboard'),

    #dashboard
    path("admindata/", views.admindata, name="admindata"),
    path("userdata/", views.userdata, name="userdata"),
    path("orderdata/", views.orderdata, name="orderdata"),
    path("productdata/", views.productdata, name="productdata"),
    path("reviewdata/", views.reviewdata, name="reviewdata"),
    
    #product
    path("addproduct/", views.addproduct, name="addproduct"),
    path("add-product/", views.add_product, name="add_product"),
    path("update-product/<int:pk>/", views.update_product, name="update_product"),
    path("delete-product/<int:pk>/", views.delete_product, name="delete_product"),

    #order
     path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
     path("order/<int:order_id>/", views.order_info, name="order_info"),
     path('order/<int:order_id>/status/<str:status>/', views.update_order_status, name='update_order_status'),
     path("orders/delete/<int:order_id>/", views.delete_order, name="delete_order"),
     path("order_list/", views.order_list, name="order_list"),

     #user
    path("userdata/<int:id>/view/", views.view_user, name="view_user"),
    path("userdata/<int:id>/edit/", views.edit_user, name="edit_user"),
    path("userdata/<int:id>/delete/", views.delete_user, name="delete_user"),


     #payment
    path("payment/", views.payment, name="payment"),
    path("payment/success/", views.payment_success, name="payment_success"),

      #report
    path('report/', views.report, name='report'),
    path("report/<str:report_type>/", views.report_view, name="report"),
]
