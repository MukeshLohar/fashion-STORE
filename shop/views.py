"""
Views for the Sri Devi Fashion Jewellery application

This module contains all views for the Sri Devi Fashion Jewellery including:
- Product catalog and search
- User authentication and profile management
- Shopping cart functionality
- Checkout and order processing
- Payment integration
"""

import json
import hashlib
import hmac
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.db.models import Q, Avg, Count
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

# Import payment libraries
import razorpay
try:
    import paypalrestsdk
except ImportError:
    paypalrestsdk = None

from .models import Product, Category, Order, OrderItem, UserProfile, Review, Wishlist
from .forms import (
    UserProfileForm, CheckoutForm, 
    CartAddProductForm, ProductReviewForm, ProductSearchForm
)
from .cart import Cart
from .currency import get_currency, set_currency, convert_price, format_price


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Decimal objects"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def safe_json_response(data, **kwargs):
    """Create a JsonResponse that can handle Decimal objects"""
    return JsonResponse(data, encoder=DecimalEncoder, **kwargs)


class ProductListView(ListView):
    """Display list of all available products with pagination"""
    model = Product
    template_name = 'shop/product_list_enhanced.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Filter products that are available"""
        return Product.objects.filter(available=True).select_related('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_products'] = Product.objects.filter(
            available=True
        ).order_by('-created_at')[:4]
        return context


class PremiumHomeView(TemplateView):
    """Premium homepage with luxury design inspired by Mia by Tanishq"""
    template_name = 'shop/premium_home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_products'] = Product.objects.filter(
            available=True
        ).order_by('-created_at')[:6]
        context['products'] = Product.objects.filter(available=True)
        return context


class ProductDetailView(DetailView):
    """Display detailed view of a single product"""
    model = Product
    template_name = 'shop/product_detail_luxury.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Add to cart form
        context['cart_product_form'] = CartAddProductForm()
        
        # Related products from same category
        context['related_products'] = Product.objects.filter(
            category=product.category,
            available=True
        ).exclude(id=product.id)[:4]
        
        # Product reviews
        context['reviews'] = Review.objects.filter(product=product).select_related('user')
        context['review_form'] = ProductReviewForm()
        
        # Average rating
        avg_rating = Review.objects.filter(product=product).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        context['avg_rating'] = round(avg_rating, 1) if avg_rating else 0
        context['review_count'] = Review.objects.filter(product=product).count()
        
        # Check if user has already reviewed this product
        if self.request.user.is_authenticated:
            context['user_review'] = Review.objects.filter(
                product=product, user=self.request.user
            ).first()
            
            # Check if product is in wishlist
            context['in_wishlist'] = Wishlist.objects.filter(
                user=self.request.user, product=product
            ).exists()
        
        return context


class CategoryDetailView(DetailView):
    """Display products in a specific category"""
    model = Category
    template_name = 'shop/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        
        # Get products in this category with pagination
        products = Product.objects.filter(
            category=category, available=True
        ).order_by('-created_at')
        
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['products'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['page_obj'] = page_obj
        
        return context


class ProductSearchView(ListView):
    """Search products with filters"""
    model = Product
    template_name = 'shop/product_search.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """Filter products based on search criteria"""
        queryset = Product.objects.filter(available=True)
        form = ProductSearchForm(self.request.GET)
        
        if form.is_valid():
            query = form.cleaned_data.get('query')
            category = form.cleaned_data.get('category')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            size = form.cleaned_data.get('size')
            color = form.cleaned_data.get('color')
            
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__name__icontains=query) |
                    Q(brand__icontains=query)
                )
            
            if category:
                queryset = queryset.filter(category__slug=category)
            
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            
            if size:
                queryset = queryset.filter(size=size)
            
            if color:
                queryset = queryset.filter(color=color)
        
        return queryset.select_related('category').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProductSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        
        # Add search query to context for display
        query = self.request.GET.get('query', '')
        context['search_query'] = query
        
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile display view"""
    template_name = 'shop/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        context['recent_orders'] = Order.objects.filter(
            user=self.request.user
        ).order_by('-created_at')[:5]
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """User profile edit view"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'shop/profile_edit.html'
    success_url = reverse_lazy('shop:profile')

    def get_object(self):
        """Get the user's profile"""
        return self.request.user.userprofile

    def form_valid(self, form):
        """Add success message"""
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)


# Shopping Cart Views

class CartDetailView(TemplateView):
    """Display shopping cart contents"""
    template_name = 'shop/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context


class CartAddView(View):
    """Add product to cart"""
    
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        
        # Check if product is available and in stock
        if not product.available:
            messages.error(request, f'{product.name} is not available.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return safe_json_response({'success': False, 'message': f'{product.name} is not available.'})
            referer = request.META.get('HTTP_REFERER')
            return redirect(referer) if referer else redirect('shop:product_list')
        
        if product.stock <= 0:
            messages.error(request, f'{product.name} is out of stock.')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return safe_json_response({'success': False, 'message': f'{product.name} is out of stock.'})
            referer = request.META.get('HTTP_REFERER')
            return redirect(referer) if referer else redirect('shop:product_list')
        
        form = CartAddProductForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            quantity = cd['quantity']
            
            # Check if requested quantity is available
            if quantity > product.stock:
                messages.error(request, f'Only {product.stock} units of {product.name} available in stock.')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return safe_json_response({
                        'success': False, 
                        'message': f'Only {product.stock} units available.'
                    })
                referer = request.META.get('HTTP_REFERER')
                return redirect(referer) if referer else redirect('shop:product_list')
            
            cart.add(
                product=product,
                quantity=quantity,
                override_quantity=cd.get('override', False)
            )
            messages.success(request, f'{product.name} added to cart successfully!')
        else:
            # Handle form validation errors - if only quantity is provided, use defaults
            quantity = request.POST.get('quantity', '1')
            try:
                quantity = int(quantity)
                if quantity > 0:
                    # Check if requested quantity is available
                    if quantity > product.stock:
                        messages.error(request, f'Only {product.stock} units of {product.name} available in stock.')
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return safe_json_response({
                                'success': False,
                                'message': f'Only {product.stock} units available.'
                            })
                        referer = request.META.get('HTTP_REFERER')
                        return redirect(referer) if referer else redirect('shop:product_list')
                    
                    cart.add(
                        product=product,
                        quantity=quantity,
                        override_quantity=False
                    )
                    messages.success(request, f'{product.name} added to cart successfully!')
                else:
                    messages.error(request, 'Invalid quantity')
            except (ValueError, TypeError):
                messages.error(request, 'Invalid quantity')
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return safe_json_response({
                'success': True,
                'cart_count': len(cart),
                'cart_total': cart.get_total_price_float(),
                'message': f'{product.name} added to cart!'
            })
        
        # Redirect back to the previous page or product list
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('shop:product_list')


class CartRemoveView(View):
    """Remove product from cart"""
    
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        messages.success(request, f'{product.name} removed from cart!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return safe_json_response({
                'success': True,
                'cart_count': len(cart),
                'message': f'{product.name} removed from cart!'
            })
        
        return redirect('shop:cart_detail')


class CartUpdateView(View):
    """Update product quantity in cart"""
    
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart.update(product, quantity)
            messages.success(request, 'Cart updated!')
        else:
            cart.remove(product)
            messages.success(request, f'{product.name} removed from cart!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return safe_json_response({
                'success': True,
                'cart_count': len(cart),
                'cart_total': cart.get_total_price_float(),
                'message': 'Cart updated!'
            })
        
        return redirect('shop:cart_detail')


class CartClearView(View):
    """Clear all items from cart"""
    
    def post(self, request):
        cart = Cart(request)
        cart.clear()
        messages.success(request, 'Cart cleared!')
        return redirect('shop:cart_detail')


# Checkout and Order Views

class CheckoutView(LoginRequiredMixin, TemplateView):
    """Checkout page with order form"""
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        
        if cart.is_empty():
            messages.error(self.request, 'Your cart is empty!')
            return redirect('shop:cart_detail')
        
        context['cart'] = cart
        context['checkout_form'] = CheckoutForm(user=self.request.user)
        return context

    def dispatch(self, request, *args, **kwargs):
        """Check if cart is not empty"""
        cart = Cart(request)
        if cart.is_empty():
            messages.error(request, 'Your cart is empty!')
            return redirect('shop:cart_detail')
        return super().dispatch(request, *args, **kwargs)


class OrderCreateView(LoginRequiredMixin, View):
    """Create a new order"""
    
    def post(self, request):
        cart = Cart(request)
        
        if cart.is_empty():
            messages.error(request, 'Your cart is empty!')
            return redirect('shop:cart_detail')
        
        form = CheckoutForm(request.POST, user=request.user)
        
        if form.is_valid():
            # Check stock availability before creating order
            for item in cart:
                product = item['product']
                if product.stock < item['quantity']:
                    messages.error(
                        request, 
                        f"Sorry, {product.name} only has {product.stock} items in stock. Please update your cart."
                    )
                    return redirect('shop:cart_detail')
            
            # Create the order
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            # Calculate shipping based on pincode
            order.shipping_cost = cart.get_shipping_cost(
                country=order.country, 
                pincode=order.postal_code
            )
            order.tax_amount = cart.get_tax_amount()
            order.save()
            
            # Save address to user profile for future use
            if hasattr(request.user, 'userprofile'):
                profile = request.user.userprofile
                profile.phone = order.phone
                profile.address_line_1 = order.address_line_1
                profile.address_line_2 = order.address_line_2
                profile.city = order.city
                profile.state = order.state
                profile.postal_code = order.postal_code
                profile.country = order.country
                profile.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Reduce product stock (safe now because we checked availability)
            for item in cart:
                product = item['product']
                product.stock -= item['quantity']
                product.save()
            
            # Clear the cart
            cart.clear()
            
            # Redirect to payment based on payment method
            if order.payment_method == 'razorpay':
                return redirect('shop:razorpay_payment', order_number=order.order_number)
            elif order.payment_method == 'paypal':
                return redirect('shop:paypal_payment', order_number=order.order_number)
            else:
                messages.error(request, 'Invalid payment method selected.')
                return redirect('shop:checkout')
        
        # If form is not valid, return to checkout
        return render(request, 'shop/checkout.html', {
            'checkout_form': form,
            'cart': cart
        })


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Display order details"""
    model = Order
    template_name = 'shop/order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

    def get_queryset(self):
        """Only show orders belonging to the current user"""
        return Order.objects.filter(user=self.request.user)


class OrderHistoryView(LoginRequiredMixin, ListView):
    """Display user's order history"""
    model = Order
    template_name = 'shop/order_history.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        """Return orders for the current user"""
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


# Payment Views

class RazorpayPaymentView(LoginRequiredMixin, TemplateView):
    """Razorpay payment processing"""
    template_name = 'shop/razorpay_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number')
        order = get_object_or_404(Order, order_number=order_number, user=self.request.user)
        
        # Initialize Razorpay client
        
        client :razorpay.Client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create Razorpay order
        razorpay_order = client.order.create({
            'amount': int(order.get_total_cost() * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': order.order_number,
            'notes': { "order_id": str(order.id) },
            'payment_capture': '1'
        })
        
        context.update({
            'order': order,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': int(order.get_total_cost() * 100),
            'currency': 'INR'
        })
        
        return context


@csrf_exempt
def razorpay_verify(request):
    """Verify Razorpay payment - Function-based view for reliability"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Get payment details from request
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        order_number = request.POST.get('order_number')
        
        if not all([payment_id, order_id, signature, order_number]):
            messages.error(request, 'Missing payment information.')
            return redirect('shop:payment_failed')
        
        # Get the order
        order = get_object_or_404(Order, order_number=order_number)
        
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Verify signature
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
            
            # Payment successful
            order.payment_status = 'paid'
            order.payment_id = payment_id
            order.status = 'processing'
            order.save()
            
            messages.success(request, 'Payment successful! Your order is being processed.')
            return redirect('shop:payment_success', order_number=order.order_number)
            
        except razorpay.errors.SignatureVerificationError:
            # Payment verification failed
            order.payment_status = 'failed'
            order.save()
            messages.error(request, 'Payment verification failed!')
            return redirect('shop:payment_failed')
            
    except Exception as e:
        messages.error(request, f'Payment processing error: {str(e)}')
        return redirect('shop:payment_failed')


class RazorpayVerifyView(View):
    """Verify Razorpay payment - DEPRECATED: Use razorpay_verify function instead"""
    http_method_names = ['get', 'post']
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request):
        """Handle GET requests with error message"""
        messages.error(request, 'Invalid payment verification request. Please complete payment through checkout.')
        return redirect('shop:cart_detail')
    
    def post(self, request):
        try:
            # Get payment details from request
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            order_number = request.POST.get('order_number')
            
            # Get the order
            order = get_object_or_404(Order, order_number=order_number)
            
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Verify signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            try:
                client.utility.verify_payment_signature(params_dict)
                
                # Payment successful
                order.payment_status = 'paid'
                order.payment_id = payment_id
                order.status = 'processing'
                order.save()
                
                messages.success(request, 'Payment successful! Your order is being processed.')
                return redirect('shop:payment_success', order_number=order.order_number)
                
            except razorpay.errors.SignatureVerificationError:
                # Payment verification failed
                order.payment_status = 'failed'
                order.save()
                messages.error(request, 'Payment verification failed!')
                return redirect('shop:payment_failed')
                
        except Exception as e:
            messages.error(request, f'Payment processing error: {str(e)}')
            return redirect('shop:payment_failed')


class PayPalPaymentView(LoginRequiredMixin, View):
    """PayPal payment processing"""
    
    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        
        if not paypalrestsdk:
            messages.error(request, 'PayPal is not configured!')
            return redirect('shop:payment_failed')
        
        # Configure PayPal SDK
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        
        # Create PayPal payment
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": request.build_absolute_uri(
                    reverse('shop:paypal_return') + f'?order_number={order.order_number}'
                ),
                "cancel_url": request.build_absolute_uri(reverse('shop:paypal_cancel'))
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"Order {order.order_number}",
                        "sku": order.order_number,
                        "price": str(order.get_total_cost()),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(order.get_total_cost()),
                    "currency": "USD"
                },
                "description": f"Sri Devi Fashion Jewellery Order {order.order_number}"
            }]
        })
        
        if payment.create():
            # Store payment ID in order
            order.payment_id = payment.id
            order.save()
            
            # Redirect to PayPal
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            messages.error(request, 'PayPal payment creation failed!')
            return redirect('shop:payment_failed')


class PayPalReturnView(LoginRequiredMixin, View):
    """Handle PayPal return after payment"""
    
    def get(self, request):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        order_number = request.GET.get('order_number')
        
        if not all([payment_id, payer_id, order_number]):
            messages.error(request, 'Invalid PayPal response!')
            return redirect('shop:payment_failed')
        
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        
        # Configure PayPal SDK
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        
        # Execute payment
        payment = paypalrestsdk.Payment.find(payment_id)
        
        if payment.execute({"payer_id": payer_id}):
            # Payment successful
            order.payment_status = 'paid'
            order.status = 'processing'
            order.save()
            
            messages.success(request, 'PayPal payment successful!')
            return redirect('shop:payment_success', order_number=order.order_number)
        else:
            # Payment failed
            order.payment_status = 'failed'
            order.save()
            messages.error(request, 'PayPal payment failed!')
            return redirect('shop:payment_failed')


class PayPalCancelView(TemplateView):
    """Handle PayPal payment cancellation"""
    template_name = 'shop/payment_cancelled.html'

    def get(self, request, *args, **kwargs):
        messages.info(request, 'PayPal payment was cancelled.')
        return super().get(request, *args, **kwargs)


class PaymentSuccessView(LoginRequiredMixin, TemplateView):
    """Payment success page"""
    template_name = 'shop/payment_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_number = kwargs.get('order_number')
        context['order'] = get_object_or_404(
            Order, order_number=order_number, user=self.request.user
        )
        return context


class PaymentFailedView(TemplateView):
    """Payment failed page"""
    template_name = 'shop/payment_failed.html'


# Wishlist Views

class WishlistView(LoginRequiredMixin, ListView):
    """Display user's wishlist"""
    model = Wishlist
    template_name = 'shop/wishlist.html'
    context_object_name = 'wishlist_items'

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')


class WishlistAddView(LoginRequiredMixin, View):
    """Add product to wishlist"""
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user, product=product
        )
        
        if created:
            messages.success(request, f'{product.name} added to wishlist!')
        else:
            messages.info(request, f'{product.name} is already in your wishlist!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return safe_json_response({
                'success': True,
                'created': created,
                'message': f'{product.name} added to wishlist!' if created else f'{product.name} is already in your wishlist!'
            })
        
        return redirect('shop:product_detail', slug=product.slug)


class WishlistRemoveView(LoginRequiredMixin, View):
    """Remove product from wishlist"""
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Wishlist.objects.filter(user=request.user, product=product).delete()
        messages.success(request, f'{product.name} removed from wishlist!')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return safe_json_response({
                'success': True,
                'message': f'{product.name} removed from wishlist!'
            })
        
        return redirect('shop:wishlist')


# Review Views

class ProductReviewView(LoginRequiredMixin, View):
    """Add or update product review"""
    
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = ProductReviewForm(request.POST)
        
        if form.is_valid():
            review, created = Review.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'title': form.cleaned_data['title'],
                    'comment': form.cleaned_data['comment']
                }
            )
            
            if not created:
                # Update existing review
                review.rating = form.cleaned_data['rating']
                review.title = form.cleaned_data['title']
                review.comment = form.cleaned_data['comment']
                review.save()
                messages.success(request, 'Your review has been updated!')
            else:
                messages.success(request, 'Thank you for your review!')
        else:
            messages.error(request, 'Please fix the errors in your review.')
        
        return redirect('shop:product_detail', slug=slug)


# Currency Views

class CurrencySwitchView(View):
    """Switch between INR and USD"""
    
    def post(self, request):
        currency = request.POST.get('currency', 'INR')
        if set_currency(request, currency):
            messages.success(request, f'Currency switched to {currency}')
        
        # Redirect back to previous page
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect('shop:home')


# AJAX Views

@require_http_methods(["POST"])
def calculate_shipping_ajax(request):
    """
    AJAX endpoint to calculate shipping cost based on pincode/postal code
    Returns: JSON with shipping cost, country, and total weight
    
    Flow:
    1. Get postal code and country from form
    2. Try to lookup postal code in database to get country
    3. If postal code not found, use country from form (required)
    4. Calculate shipping based on country rate × weight
    """
    try:
        postal_code = request.POST.get('pincode', '').strip()  # Form field name is postal_code
        form_country = request.POST.get('country', '').strip()
        
        if not postal_code:
            return safe_json_response({
                'success': False,
                'error': 'Postal code is required'
            })
        
        if not form_country:
            return safe_json_response({
                'success': False,
                'error': 'Country is required'
            })
        
        # Get cart
        cart = Cart(request)
        if cart.is_empty():
            return safe_json_response({
                'success': False,
                'error': 'Cart is empty'
            })
        
        # Calculate shipping cost
        cart_total = cart.get_total_price()
        total_weight = cart.get_total_weight()
        
        # Import here to avoid circular import
        from .models import PincodeZone, ShippingRate
        
        # Try to get country from postal code database
        # If not found, use country from form
        try:
            pincode_obj = PincodeZone.objects.get(pincode=postal_code)
            detected_country = pincode_obj.country
            pincode_found = True
        except PincodeZone.DoesNotExist:
            detected_country = form_country
            pincode_found = False
        
        # Calculate shipping
        shipping_cost = ShippingRate.calculate_shipping_cost(
            cart_total=cart_total,
            country=detected_country,
            pincode=postal_code,
            total_weight_kg=total_weight
        )
        
        return safe_json_response({
            'success': True,
            'shipping_cost': float(shipping_cost),
            'country': detected_country,
            'total_weight_kg': float(total_weight),
            'cart_total': float(cart_total),
            'formatted_shipping': f'₹{shipping_cost:,.2f}',
            'pincode_found': pincode_found,
            'message': f'Shipping to {detected_country}' + (' (postal code verified)' if pincode_found else '')
        })
        
    except Exception as e:
        return safe_json_response({
            'success': False,
            'error': str(e)
        })