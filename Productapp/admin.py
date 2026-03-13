from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'price',
        'stock',
        'category',
        'subcategory',  # ✅ Added subcategory here
        'is_available',
        'created_date',
        'modified_date',
    )
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'category__category_name', 'subcategory__subcategory_name')
    list_filter = ('category', 'subcategory', 'is_available')
    list_per_page = 25
