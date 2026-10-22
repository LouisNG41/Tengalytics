from django.contrib import admin
from collection.models import Product, Purchase, PriceSnapshot

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nom", "tcg", "cardmarket_id", "category", "serie")
    search_fields = ("nom", "cardmarket_id", "serie")


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("date_purchase", "price_purchase", "quantite", "product")
    search_fields = ("product", "price_purchase", "quantite")    

@admin.register(PriceSnapshot)
class PriceSnapshotAdmin(admin.ModelAdmin):
    list_display = ("product","price_dict")