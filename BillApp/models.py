from django.db import models

class Bill(models.Model):
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.CharField(max_length=7, help_text="MM/YYYY", blank=True, null=True)
    cvc = models.CharField(max_length=4, blank=True, null=True)
    country = models.CharField(max_length=100, default="India")
    state = models.CharField(max_length=100, default="Gujarat")
    city = models.CharField(max_length=100, default="Rajkot")
    street_address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill - {self.first_name} {self.last_name} ({self.payment_method})"
