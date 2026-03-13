from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from functools import wraps
from decimal import Decimal
import io, base64
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.http import HttpResponse

from Registrationapp.models import Register
from Productapp.models import Product
from categoryapp.models import Category, SubCategory
from demo.models import Order1
from BillApp.models import Bill


# ---------------------------
# Decorators
# ---------------------------
def login_required(view_func):
    """Check if user (normal or admin) is logged in."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        cname = request.session.get('cname')
        is_admin = request.session.get('is_admin', False)
        if not cname and not is_admin:
            messages.error(request, "You must log in to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Only allow admin users."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_admin', False):
            messages.error(request, "Admin access required!")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ---------------------------
# Authentication & Session
# ---------------------------
def login(request):
    return render(request, 'Login.html')


def registration(request):
    return render(request, 'Registration.html')


def regidata(request):
    if request.method != "POST":
        return redirect('registration')

    required_fields = ['id','name','password','em','mobi','city','cont','state']
    if not all(field in request.POST and request.POST[field] for field in required_fields):
        return render(request, 'Registration.html', {'status': 'error','message': 'All fields are required.'})

    cid = request.POST['id']
    cname = request.POST['name']
    cpassword = request.POST['password']
    cemail = request.POST['em']
    cmob = request.POST['mobi']
    ccity = request.POST['city']
    ccon = request.POST['cont']
    cstate = request.POST['state']

    if Register.objects.filter(cid=cid).exists():
        return render(request, 'Registration.html', {
            'status': 'error',
            'message': 'User already registered. Please login.'
        })

    Register.objects.create(
        cid=cid, cname=cname, cpassword=cpassword, cemail=cemail,
        cmob=cmob, ccity=ccity, ccon=ccon, cstate=cstate
    )

    return render(request, 'Registration.html', {'status': 'success','message': 'Registration successful!'})


def logincheck(request):
    if request.method != "POST":
        return redirect('login')

    cname = request.POST.get('name')
    password = request.POST.get('password')

    # Admin login
    if cname == "admin" and password == "Admin123":
        request.session['cname'] = cname
        request.session['is_admin'] = True
        messages.success(request, f"Welcome Admin {cname}!")
        return redirect('dashboard')

    # Normal user login
    try:
        user = Register.objects.get(cname=cname, cpassword=password)
        request.session['cname'] = user.cname
        request.session['is_admin'] = getattr(user, 'is_admin', False)  # optional if you track admin in model
        messages.success(request, f"Welcome {user.cname}!")
        return redirect('home')
    except Register.DoesNotExist:
        messages.error(request, "Invalid username or password")
        return render(request, 'Login.html',{"error": "Login failed"})


#@never_cache
#def custom_logout(request):
    """Logout user and flush session"""
    request.session.flush()
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

@never_cache
def logout_view(request):
    cname = request.session.get('cname')
    is_admin = request.session.get('is_admin', False)

    # Clear session
    request.session.flush()
    logout(request)

    # Redirect based on type
    if is_admin:
        messages.success(request, " logged out successfully!")
        return redirect('login')   # Login page for admin
    else:
        messages.success(request, "Logged out successfully!")
        return redirect('login')    # Public home page


# ---------------------------
# Dashboard / Home
# ---------------------------
@login_required
@admin_required
def dashboard(request):
    return render(request, 'Dashboard.html')



def home(request):
    """Normal user homepage"""
    return render(request, 'home.html')

def admindata(request):
    # your logic here
    return render(request, 'admindata.html') 
# ---------------------------
# User Management
# ---------------------------
@login_required
def userdata(request):
    users = Register.objects.all()
    return render(request, "Userdata.html", {"users": users})


@login_required
def view_user(request, id):
    get_object_or_404(Register, id=id)
    return redirect("userdata")


@login_required
def edit_user(request, id):
    user = get_object_or_404(Register, id=id)
    return render(request, "Registration.html", {"user": user})


@login_required
def delete_user(request, id):
    user = get_object_or_404(Register, id=id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted successfully!")
    return redirect("userdata")


# ---------------------------
# Product Management
# ---------------------------
@login_required
def productdata(request):
    products = Product.objects.all()
    return render(request, "Productdata.html", {"products": products})


@login_required
def addproduct(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    return render(request, "Addproductform.html", {"categories": categories, "subcategories": subcategories})


@login_required
def add_product(request):
    if request.method != "POST":
        return redirect('addproduct')

    product_name = request.POST.get("product_name")
    slug = request.POST.get("slug")
    description = request.POST.get("description")
    price = request.POST.get("price")
    gst = request.POST.get("gst")
    stock = request.POST.get("stock")
    is_available = request.POST.get("available") == "on"

    category = Category.objects.filter(id=request.POST.get("category")).first()
    subcategory = SubCategory.objects.filter(id=request.POST.get("subcategory")).first()

    Product.objects.create(
        product_name=product_name, slug=slug, description=description,
        price=price, gst=gst, stock=stock, is_available=is_available,
        category=category, subcategory=subcategory,
        image=request.FILES.get("img1"),
        car_part1=request.FILES.get("img2"),
        car_part2=request.FILES.get("img3"),
        car_part3=request.FILES.get("img4"),
    )
    messages.success(request, "Product submitted successfully!")
    return redirect("productdata")


@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    if request.method == "POST":
        product.product_name = request.POST.get("product_name")
        product.slug = request.POST.get("slug")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.gst = request.POST.get("gst")
        product.stock = request.POST.get("stock")
        product.is_available = request.POST.get("available") == "on"
        product.category = Category.objects.filter(id=request.POST.get("category")).first()
        product.subcategory = SubCategory.objects.filter(id=request.POST.get("subcategory")).first()

        for i, field in enumerate(['img1','img2','img3','img4']):
            if request.FILES.get(field):
                setattr(product, ['image','car_part1','car_part2','car_part3'][i], request.FILES.get(field))

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect("productdata")

    return render(request, "Updateproductform.html", {"product": product, "categories": categories, "subcategories": subcategories})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully!")
    return redirect("productdata")


# ---------------------------
# Order Management
# ---------------------------
@login_required
def orderdata(request):
    orders = Order1.objects.all().prefetch_related('items')
    return render(request, 'Orderdata.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order1, id=order_id)
    return render(request, "orderdata.html", {"order": order})


@login_required
def order_info(request, order_id):
    order = get_object_or_404(Order1, id=order_id)
    order_items = order.items.all()
    subtotal = sum([item.subtotal() for item in order_items])
    tax = round(subtotal * 0.18, 2)
    total = subtotal + tax
    return render(request, "order_info.html", {
        "order": order, "order_items": order_items,
        "subtotal": subtotal, "tax": tax, "total": total
    })


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order1, id=order_id)
    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted successfully!")
    return redirect('orderdata')


@login_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order1, id=order_id)
    order.status = status
    order.save()
    return redirect('orderdata')


@login_required
def order_list(request):
    orders = Order1.objects.all().order_by('-created_at')
    return render(request, "orderdata.html", {"orders": orders})


# ---------------------------
# Payment
# ---------------------------
@login_required
def payment(request):
    cname = request.session.get("cname")
    reg = get_object_or_404(Register, cname=cname) if cname else None

    if request.method == "POST":
        Bill.objects.create(
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            card_number=request.POST.get("card_number"),
            expiry_date=request.POST.get("expiry"),
            cvc=request.POST.get("cvc"),
            country=request.POST.get("country"),
            state=request.POST.get("state"),
            city=request.POST.get("city"),
            street_address=request.POST.get("street_address"),
            pincode=request.POST.get("pincode"),
        )
        messages.success(request, "Payment information saved successfully.")
        return redirect("payment_success")

    return render(request, "payment.html", {"reg": reg})


@login_required
def payment_success(request):
    return render(request, "payment_success.html")


# ---------------------------
# Reviews
# ---------------------------
@login_required
def reviewdata(request):
    return render(request, 'Reviewdata.html')


@login_required
def reviews(request):
    return render(request,'review.html')


# ---------------------------
# Reporting
# ---------------------------
def generate_chart(data, labels, title):
    fig, ax = plt.subplots()
    ax.bar(labels, data, color="skyblue")
    ax.set_title(title)
    ax.set_ylabel("Values")
    ax.set_xlabel("Id")

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode("utf-8")


@login_required
def report(request):
    return render(request,"Report.html")


@login_required
def report_view(request, report_type="stock"):
    stock_qs = Product.objects.all()
    stock_data = [["Product ID","Product", "Stock"]] + [[p.id,p.product_name, p.stock] for p in stock_qs]

    order_qs = Order1.objects.all()
    order_data = [["Order ID", "Customer", "Total Price", "Status", "Date"]] + [
        [o.id, o.customer_name, str(o.total_price), o.status, o.created_at.strftime("%Y-%m-%d")] for o in order_qs
    ]

    sales_data = [["Product", "Units Sold", "Month"], ["Hyundai Creta", 12, "Sept"], ["Hyundai Venue", 7, "Sept"], ["Hyundai Verna", 5, "Sept"]]

    reports = {"stock": stock_data, "orders": order_data, "sales": sales_data}

    if report_type == "stock":
        labels = [str(row[0]) for row in stock_data[1:]]
        values = [int(row[2]) for row in stock_data[1:]]
        chart = generate_chart(values, labels, "Stock Report")
    elif report_type == "orders":
        labels = [row[0] for row in order_data[1:]]
        values = [float(row[2]) for row in order_data[1:]]
        chart = generate_chart(values, labels, "Orders Report (Total Price)")
    else:
        labels = [row[0] for row in sales_data[1:]]
        values = [row[1] for row in sales_data[1:]]
        chart = generate_chart(values, labels, "Sales Report")

    if request.GET.get("download") == "pdf":
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.pdf"'
        doc = SimpleDocTemplate(response)
        styles = getSampleStyleSheet()
        elements = [Paragraph(f"{report_type.capitalize()} Report", styles['Title']), Spacer(1,12)]
        table = Table(reports[report_type])
        table.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.lightblue),
                                   ("GRID",(0,0),(-1,-1),1,colors.black),
                                   ("ALIGN",(0,0),(-1,-1),"CENTER")]))
        elements.append(table)
        elements.append(Spacer(1,20))
        doc.build(elements)
        return response

    return render(request, "report.html", {"report_type": report_type, "data": reports[report_type], "chart": chart})
