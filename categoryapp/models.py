from django.db import models
from django.urls import reverse

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    category_image = models.ImageField(upload_to='photos/categories/', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        return reverse('productcats',args=[self.slug])   

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    subcategory_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    subcategory_image = models.ImageField(upload_to='photos/subcategories/', blank=True)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return f"{self.category.category_name} → {self.subcategory_name}"
