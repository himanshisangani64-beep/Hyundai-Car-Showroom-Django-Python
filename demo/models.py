# demo/models.py
from django.db import models
from Productapp.models import Product


class Order1(models.Model):
    customer_name = models.CharField(max_length=100, blank=False, null=False)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"


class OrderItem1(models.Model):
    order = models.ForeignKey(Order1, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        """
        Reduce stock automatically when a new order item is created.
        """
        if not self.pk:  # only on first creation, not updates
            if self.product.stock >= self.quantity:
                self.product.stock -= self.quantity
                self.product.save()
            else:
                raise ValueError("Not enough stock available")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OrderItem: {self.product} x {self.quantity}"
