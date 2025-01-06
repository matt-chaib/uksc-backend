from django.contrib import admin
from .models import Supplier

# Register the Supplier model with the admin site
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'address', 'country', 'workers', 'sector')
    search_fields = ('supplier', 'country', 'sector')