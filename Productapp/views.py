from django.shortcuts import render, get_object_or_404
from .models import Product
from categoryapp.models import Category, SubCategory

def product_list_view(request, category_slug=None):
    selected_category = None
    products = Product.objects.filter(is_available=True)

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    products = products[:12]  # Limit to 12
    total_products = products.count()
    slide_width_percentage = 100 / total_products if total_products > 0 else 100

    context = {
        'products': products,
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'slide_width_percentage': slide_width_percentage,
        'selected_category': selected_category,
    }

    return render(request, 'product.html', context)

def pro_info(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_info.html', {'product': product})
