# cartapp/models.py

from django.db import models
from Productapp.models import Product
from Registrationapp.models import Register
from demo.models import Order1


class Cart(models.Model):
    cid = models.OneToOneField(Register, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250, blank=True, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    order = models.ForeignKey(Order1, on_delete=models.SET_NULL, null=True, blank=True)

    def sub_total(self):
        """Calculate total price for this cart item"""
        return self.product.price * self.quantity
    
    def get_product_id(self):
        """Fetch Product ID (useful in admin/list_display)"""
        return self.product.id
    get_product_id.short_description = "Product ID"

    def __str__(self):
        # FIX: use product_name instead of name
        return f"{self.product.product_name} (ID: {self.product.id})"
