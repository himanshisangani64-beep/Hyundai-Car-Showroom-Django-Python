from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    if 'admin' in request.path:
        return {}

    cart_count = 0  # Always initialize

    try:
        cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
        if cart:
            cart_items = CartItem.objects.filter(cart=cart)
            # Sum the quantities of all items
            cart_count = sum(item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_count = 0

    return {'cart_count': cart_count}
