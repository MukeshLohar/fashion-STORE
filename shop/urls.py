"""
URL configuration for the shop app

This module defines all URL patterns for the Sri Devi Fashion Jewellery:
- Product catalog and search
- User authentication and profile
- Shopping cart and checkout
- Order management
- Payment processing
"""

from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Home and product catalog
    path('', views.PremiumHomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/page/<int:page>/', views.ProductListView.as_view(), name='product_list_paginated'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    
    # User profile (keeping these as they're custom)
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    
    # Shopping cart
    path('cart/', views.CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/update/<int:product_id>/', views.CartUpdateView.as_view(), name='cart_update'),
    path('cart/clear/', views.CartClearView.as_view(), name='cart_clear'),
    
    # Checkout and orders
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/<str:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/', views.OrderHistoryView.as_view(), name='order_history'),
    
    # Payment processing
    path('payment/razorpay/verify/', views.razorpay_verify, name='razorpay_verify'),
    path('payment/razorpay/<str:order_number>/', views.RazorpayPaymentView.as_view(), name='razorpay_payment'),
    path('payment/paypal/<str:order_number>/', views.PayPalPaymentView.as_view(), name='paypal_payment'),
    path('payment/paypal/return/', views.PayPalReturnView.as_view(), name='paypal_return'),
    path('payment/paypal/cancel/', views.PayPalCancelView.as_view(), name='paypal_cancel'),
    path('payment/success/<str:order_number>/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('payment/failed/', views.PaymentFailedView.as_view(), name='payment_failed'),
    
    # Shipping calculation
    path('ajax/calculate-shipping/', views.calculate_shipping_ajax, name='calculate_shipping_ajax'),
    
    # Wishlist
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.WishlistAddView.as_view(), name='wishlist_add'),
    path('wishlist/remove/<int:product_id>/', views.WishlistRemoveView.as_view(), name='wishlist_remove'),
    
    # Reviews
    path('product/<slug:slug>/review/', views.ProductReviewView.as_view(), name='product_review'),
    
    # Currency
    path('currency/switch/', views.CurrencySwitchView.as_view(), name='currency_switch'),
]