from django.contrib import admin
from .models import Product, Order, ContactMessage

admin.site.register(Product)

admin.site.register(ContactMessage)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'created_at', 'address')
    search_fields = ('user__username', 'product__name')