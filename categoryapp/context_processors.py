from .models import Category  # Import your model

def menu_links(request):
    links = Category.objects.all()
    return {'links': links}
