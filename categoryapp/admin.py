from django.contrib import admin
from .models import Category, SubCategory

# Admin for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'slug')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name',)
    list_per_page = 20
    ordering = ('category_name',)


# Admin for SubCategory
@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory_name', 'category', 'slug')
    prepopulated_fields = {'slug': ('subcategory_name',)}
    search_fields = ('subcategory_name', 'category__category_name')
    list_filter = ('category',)
    list_per_page = 20
    ordering = ('subcategory_name',)
