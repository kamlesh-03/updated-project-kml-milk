from django.contrib import admin
from .models import Category, Product, FarmContent, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_en", "slug")
    prepopulated_fields = {"slug": ("name_en",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "pack_size", "unit", "price", "stock_qty", "expiry_days", "active")
    list_filter = ("section", "active")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price", "stock_qty", "expiry_days", "active")

@admin.register(FarmContent)
class FarmContentAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "published_at")
    prepopulated_fields = {"slug": ("title",)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "phone", "email")
    inlines = [OrderItemInline]
