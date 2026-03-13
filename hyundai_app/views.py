from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
from datetime import datetime
from num2words import num2words
from decimal import Decimal, ROUND_HALF_UP
import os

from demo.models import Order1, OrderItem1  # Your models


def _get_invoice_context(order, is_pdf=False):
    """Prepare common context data for invoice templates."""
    order_item = OrderItem1.objects.filter(order=order).first()

    subtotal = Decimal(order.total_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    tax = (subtotal * Decimal("0.20")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    grand_total = (subtotal + tax).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    # Convert amount to words (Indian format)
    amount_in_words = num2words(grand_total, lang="en_IN").title() + " Only"

    return {
        "order": order,
        "order_item": order_item,
        "car_model": "Hyundai Creta",
        "price": order_item.price if order_item else 0,
        "subtotal": subtotal,
        "tax": tax,
        "grand_total": grand_total,
        "amount_in_words": amount_in_words,
        "date": datetime.now().strftime("%d-%m-%Y"),
        "is_pdf": is_pdf,
    }


def view_bill(request, order_id):
    """Render invoice in browser as HTML (with payment button)."""
    order = get_object_or_404(Order1, id=order_id)
    context = _get_invoice_context(order, is_pdf=False)
    return render(request, "Bill1.html", context)


def generate_bill(request, order_id):
    """Generate invoice as PDF and return inline in browser."""
    order = get_object_or_404(Order1, id=order_id)
    context = _get_invoice_context(order, is_pdf=True)

    # Render HTML to string
    html_string = render_to_string("Bill1.html", context)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())

    # Ensure CSS is applied
    css_path = os.path.join(settings.STATIC_ROOT, "Css", "bill1.css")
    stylesheets = [CSS(filename=css_path)] if os.path.exists(css_path) else None

    # Generate PDF
    pdf_file = html.write_pdf(stylesheets=stylesheets)

    # Save PDF to media/bills folder
    bills_folder = os.path.join(settings.MEDIA_ROOT, "bills")
    os.makedirs(bills_folder, exist_ok=True)

    filename = f"invoice_{order.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(bills_folder, filename)
    with open(filepath, "wb") as f:
        f.write(pdf_file)

    # Return inline PDF response
    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="{filename}"'
    return response
