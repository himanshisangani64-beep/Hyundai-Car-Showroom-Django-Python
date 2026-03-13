from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from Productapp.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Registrationapp.models import Register  #
import uuid

# Helper: Get session-based cart_id
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def addtocart(request):
    # Add your cart logic here (e.g., fetch cart, add item, etc.)
    return render(request, 'add_to_cart.html') 

# View: Cart page
def cart(request):
    total_price = 0
    quantity = 0
    cart_items = []
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total_price += item.product.price * item.quantity
            quantity += item.quantity
    except ObjectDoesNotExist:
        pass

    tax_rate = 0.28 # 18% tax
    tax_amount = total_price * tax_rate/100
    total = total_price + tax_amount

    context = {
        'total_price': total_price,
        'tax_amount': tax_amount,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'add_to_cart.html', context)
# remove cart 

def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect('cart')  # Or some fallback

    cart_item = CartItem.objects.filter(product=product, cart=cart).first()

    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    else:
        messages.warning(request, "This item is not in your cart.")

    return redirect('cart')      

# View: Add to cart
def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)

    return redirect('cart')

def remove_cart_item(request,product_id):
     cart = Cart.objects.get(cart_id=_cart_id(request))
     product = get_object_or_404(Product, id=product_id)
     cart_item = CartItem.objects.get(product=product, cart=cart)
     cart_item.delete()
     return redirect('cart')



def checkout(request):
    total_price = 0
    quantity = 0
    reg = None  
    cart_items = []
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total_price += item.product.price * item.quantity
            quantity += item.quantity
        reg = None
        if request.session.get('cname'):
           cname = request.session['cname']
           reg = get_object_or_404(Register, cname=cname)  
    except ObjectDoesNotExist:
        pass

    tax_rate = 0.28 # 18% tax
    tax_amount = total_price * tax_rate/100
    total = total_price + tax_amount

    context = {
        'total_price': total_price,
        'tax_amount': tax_amount,
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'reg': reg,
    }
    return render(request, 'checkout.html', context)


def registration1(request):
    return render(request, 'Registration1.html')

def login1(request):
    next_url = request.GET.get('next', '/')
    return render(request, 'Login1.html', {'next': next_url})

def pro_info1(request):
    # ✅ Safely get product ID from query or session or default to 1
    product_id = request.GET.get('id') or 1

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        product = None

    return render(request, 'product_info.html', {'product': product})

def regidata1(request):
    if request.method == 'POST':
        cid = request.POST.get('id')
        cname = request.POST.get('name')
        cpassword = request.POST.get('password')
        cemail = request.POST.get('em')
        cmob = request.POST.get('mobi')
        ccity = request.POST.get('city')
        ccon = request.POST.get('cont')
        cstate = request.POST.get('state')

        if cid and cname and cpassword and cemail and cmob and ccity and ccon and cstate:
            if Register.objects.filter(cid=cid).exists():
                # User already exists
                return render(request, 'Registration1.html', {
                    'status': 'error',
                    'message': 'User  already registered. Please login.'
                })

            Register.objects.create(
                cid=cid,
                cname=cname,
                cpassword=cpassword,
                cemail=cemail,
                cmob=cmob,
                ccity=ccity,
                ccon=ccon,
                cstate=cstate
            )

            # Registration successful
            return render(request, 'Registration1.html', {
                'status': 'success',
                'message': 'Registration successful!'
            })

        else:
            return render(request, 'Registration1.html', {
                'status': 'error',
                'message': 'All fields are required.'
            })

    return redirect('registration1')

from Productapp.models import Product  # or wherever your Product model is defined

def logincheck1(request):
    if request.method == 'POST':
        cname = request.POST.get('name')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(cname=cname, cpassword=password)
            request.session['cname'] = cname
            request.session['is_admin'] = user.is_admin  # if you have this field

            
            if cname == "admin" and password == "Admin123":
                return redirect('dashboard')  # Admin dashboard
            else:
                return redirect('pro_info1')  # Redirect to next or product_info

        except Register.DoesNotExist:
            return render(request, 'Login1.html', {'error': 'Invalid name or password'})

    return redirect('login1')







