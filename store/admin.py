from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Customer, Category, Product, Brand, 
    ProductImage, Review, Cart, Order, Wishlist
)

@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff')
    search_fields = ('username', 'email', 'phone')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'product_count')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock_count', 'on_sale')
    list_filter = ('category', 'brand', 'on_sale')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'created_at')

admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Wishlist)