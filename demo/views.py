from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal
from datetime import datetime

from .models import Order1, OrderItem1
from Productapp.models import Product
from cartapp.models import Cart, CartItem
from cartapp.views import _cart_id   # make sure this exists in cartapp


def place_order1(request):
    if request.method == "POST":
        try:
            # Create order
            order = Order1.objects.create(
                customer_name=request.POST.get("customer_name"),
                address=request.POST.get("address"),
                phone=request.POST.get("phone"),
                email=request.POST.get("email"),
                city=request.POST.get("city"),
                state=request.POST.get("state"),
                country=request.POST.get("country"),
                total_price=request.POST.get("total"),
                status="Pending"
            )

            # Save order items
            products_data = request.POST.getlist("products[]")
            for product_str in products_data:
                pid, qty, subtotal = product_str.split("|")
                product = Product.objects.get(id=pid)

                OrderItem1.objects.create(
                    order=order,
                    product=product,
                    quantity=int(qty),
                    price=product.price
                )

            messages.success(request, f"✅ Order #{order.id} placed successfully!")
            return redirect("order_success", order_id=order.id)

        except Exception as e:
            print("⚠️ Order error:", e)
            messages.error(request, f"⚠️ Failed to place order: {e}")
            return redirect("checkout")

    return redirect("checkout")


def order_success(request, order_id):
    try:
        order = Order1.objects.get(id=order_id)
    except Order1.DoesNotExist:
        messages.error(request, "⚠️ That order does not exist or was already removed.")
        return redirect("product")  # or some fallback page

    order_items = OrderItem1.objects.filter(order=order)

    subtotal = sum([item.price * item.quantity for item in order_items], Decimal("0.00"))
    tax_rate = Decimal("0.09")  # 9% GST
    tax = (subtotal * tax_rate).quantize(Decimal("0.01"))
    total = subtotal + tax

    context = {
        "order": order,
        "order_items": order_items,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "date": getattr(order, "created_at", datetime.now()),
    }
    return render(request, "Bill.html", context)



def remove_order_item(request, order_id, product_id):
    order = get_object_or_404(Order1, id=order_id)
    product = get_object_or_404(Product, id=product_id)

    # Find order item
    order_item = OrderItem1.objects.filter(order=order, product=product).first()
    if order_item:
        # 🔹 Restore stock
        product.stock += order_item.quantity
        product.save()

        order_item.delete()

    # Remove from cart too
    cart = Cart.objects.filter(cart_id=_cart_id(request)).first()
    if cart:
        CartItem.objects.filter(cart=cart, product=product).delete()

    #  If no items left → delete order & redirect to product page
    if not OrderItem1.objects.filter(order=order).exists():
        order.delete()
        messages.success(request, " All items removed. Your order was canceled. Continue shopping!")
        return redirect("product")

    #  Otherwise → back to order success page
    messages.success(request, f" {product.product_name} removed from Order #{order.id} and stock updated.")
    return redirect("order_success", order_id=order.id)

