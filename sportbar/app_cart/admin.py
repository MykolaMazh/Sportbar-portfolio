from django.contrib import admin

from app_cart.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("deliver_by", "is_delivered", "is_paid")
    ordering = ["deliver_by"]
    list_editable = ["is_delivered", "is_paid"]
    list_filter = ["is_delivered", "is_paid"]
