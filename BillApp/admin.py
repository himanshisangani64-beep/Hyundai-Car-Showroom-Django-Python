from django.contrib import admin
from .models import Bill   # ✅ Import your model

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "card_number",
        "expiry_date",
        "country",
        "state",
        "city",
        "pincode",
        "created_at",
    )
    search_fields = ("first_name", "last_name", "city", "pincode")
    list_filter = ( "country", "state", "city", "created_at")
