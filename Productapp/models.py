from django.db import models
from categoryapp.models import Category, SubCategory
from django.urls import reverse

class Product(models.Model):
 
    product_name     = models.CharField(max_length=200, unique=True)
    slug             = models.SlugField(max_length=200, unique=True)
    description      = models.TextField(max_length=500, blank=True)
    price            = models.IntegerField()
    gst              = models.IntegerField()
    image            = models.ImageField(upload_to='photos/products/', blank=True)
    car_part1        = models.ImageField(upload_to='photos/car_parts',blank=True)
    car_part2        = models.ImageField(upload_to='photos/car_parts',blank=True)
    car_part3        = models.ImageField(upload_to='photos/car_parts',blank=True)
    stock            = models.IntegerField(default=0)
    is_available     = models.BooleanField(default=True)

    # Relations
    category         = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory      = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)

    # Timestamps
    created_date     = models.DateField(auto_now_add=True)
    modified_date    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
       self.stock = int(self.stock) if self.stock else 0
       if self.stock <= 0:
          self.available = False
       super().save(*args, **kwargs)
   

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
