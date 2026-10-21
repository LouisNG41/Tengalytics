from django.contrib import admin
from collection.models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nom", "tcg", "cardmarket_id", "category", "serie")
    search_fields = ("nom", "cardmarket_id", "serie")