"""
Django Admin configuration for Fashion Store

This module customizes the Django admin interface for managing:
- Products and Categories
- Orders and Order Items
- Users and User Profiles
- Reviews and Wishlists
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import (
    Category, Product, UserProfile, Order, OrderItem, 
    Review, Wishlist
)


# Inline admin classes
class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ('get_cost',)
    
    def get_cost(self, obj):
        return f"₹{obj.get_cost():.2f}"
    get_cost.short_description = 'Total Cost'


class ReviewInline(admin.TabularInline):
    """Inline admin for product reviews"""
    model = Review
    extra = 0
    readonly_fields = ('created_at',)


class UserProfileInline(admin.StackedInline):
    """Inline admin for user profile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


# Main admin classes
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Categories"""
    list_display = ('name', 'slug', 'product_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    def product_count(self, obj):
        """Display number of products in category"""
        return obj.products.count()
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Products"""
    list_display = (
        'name', 'category', 'price', 'stock', 'size', 'color', 
        'available', 'image_preview', 'created_at'
    )
    list_filter = (
        'available', 'category', 'size', 'color', 'brand', 'created_at'
    )
    search_fields = ('name', 'description', 'brand', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_editable = ('price', 'stock', 'available')
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Product Details', {
            'fields': ('size', 'color', 'material', 'brand')
        }),
        ('Images', {
            'fields': ('image', 'image_2', 'image_3', 'image_preview')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ReviewInline]
    
    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'
    
    actions = ['mark_as_available', 'mark_as_unavailable', 'duplicate_products']
    
    def mark_as_available(self, request, queryset):
        """Mark selected products as available"""
        updated = queryset.update(available=True)
        self.message_user(request, f'{updated} products marked as available.')
    mark_as_available.short_description = 'Mark selected products as available'
    
    def mark_as_unavailable(self, request, queryset):
        """Mark selected products as unavailable"""
        updated = queryset.update(available=False)
        self.message_user(request, f'{updated} products marked as unavailable.')
    mark_as_unavailable.short_description = 'Mark selected products as unavailable'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Orders"""
    list_display = (
        'order_number', 'user', 'status', 'payment_status', 
        'payment_method', 'total_cost', 'created_at'
    )
    list_filter = (
        'status', 'payment_status', 'payment_method', 'created_at'
    )
    search_fields = (
        'order_number', 'user__username', 'user__email', 
        'first_name', 'last_name', 'email'
    )
    readonly_fields = (
        'order_number', 'created_at', 'updated_at', 'total_cost'
    )
    list_per_page = 50
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'created_at', 'updated_at')
        }),
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': (
                'address_line_1', 'address_line_2', 'city', 
                'state', 'postal_code', 'country'
            )
        }),
        ('Payment Information', {
            'fields': (
                'payment_method', 'payment_status', 'payment_id',
                'total_amount', 'shipping_cost', 'tax_amount', 'total_cost'
            )
        }),
        ('Delivery Information', {
            'fields': ('shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [OrderItemInline]
    
    def total_cost(self, obj):
        """Display total order cost"""
        return f"₹{obj.get_total_cost():.2f}"
    total_cost.short_description = 'Total Cost'
    
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_processing(self, request, queryset):
        """Mark orders as processing"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_as_processing.short_description = 'Mark as processing'
    
    def mark_as_shipped(self, request, queryset):
        """Mark orders as shipped"""
        from django.utils import timezone
        updated = queryset.update(status='shipped', shipped_at=timezone.now())
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_as_shipped.short_description = 'Mark as shipped'
    
    def mark_as_delivered(self, request, queryset):
        """Mark orders as delivered"""
        from django.utils import timezone
        updated = queryset.update(status='delivered', delivered_at=timezone.now())
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = 'Mark as delivered'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for Order Items"""
    list_display = ('order', 'product', 'quantity', 'price', 'get_cost')
    list_filter = ('order__status', 'order__created_at')
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('get_cost',)
    
    def get_cost(self, obj):
        """Display total cost for this item"""
        return f"₹{obj.get_cost():.2f}"
    get_cost.short_description = 'Total Cost'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Reviews"""
    list_display = ('product', 'user', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50
    
    def get_queryset(self, request):
        """Optimize queryset"""
        return super().get_queryset(request).select_related('product', 'user')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Admin interface for Wishlist"""
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('created_at',)


# Customize User admin to include profile
class CustomUserAdmin(UserAdmin):
    """Custom User admin with profile inline"""
    inlines = (UserProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        """Only show profile inline when editing existing user"""
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


# Admin site customization
admin.site.site_header = "Fashion Store Admin"
admin.site.site_title = "Fashion Store Admin Portal"
admin.site.index_title = "Welcome to Fashion Store Administration"