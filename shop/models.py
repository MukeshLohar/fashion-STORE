"""
Models for the Sri Devi Fashion Jewellery E-commerce application

This module contains all the database models for our Sri Devi Fashion Jewellery:
- Product: Fashion items with details, pricing, and images
- UserProfile: Extended user information
- Order: Customer orders
- OrderItem: Individual items within an order
"""

from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


class Category(models.Model):
    """Product categories for fashion items"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', kwargs={'slug': self.slug})


class Product(models.Model):
    """Fashion product model with all necessary details"""
    
    # Size choices for fashion items
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    # Color choices
    COLOR_CHOICES = [
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('black', 'Black'),
        ('white', 'White'),
        ('gray', 'Gray'),
        ('navy', 'Navy'),
        ('pink', 'Pink'),
        ('yellow', 'Yellow'),
        ('purple', 'Purple'),
        ('brown', 'Brown'),
        ('orange', 'Orange'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    
    # Weight in kilograms for shipping calculation
    weight_kg = models.DecimalField(
        max_digits=6, 
        decimal_places=3, 
        default=0.100,
        validators=[MinValueValidator(0.001)],
        help_text="Product weight in kilograms (e.g., 0.500 for 500g)"
    )
    
    # Fashion-specific fields
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, default='M')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='black')
    material = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    
    # Images
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    
    # SEO and metadata
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['available']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """Override save to resize images"""
        super().save(*args, **kwargs)
        
        # Resize main image
        if self.image:
            self.resize_image(self.image.path, (800, 800))
        
        # Resize additional images
        if self.image_2:
            self.resize_image(self.image_2.path, (800, 800))
            
        if self.image_3:
            self.resize_image(self.image_3.path, (800, 800))

    def resize_image(self, image_path, size):
        """Resize image to specified size while maintaining aspect ratio"""
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if image is in RGBA mode
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Resize image
                img.thumbnail(size, Image.Resampling.LANCZOS)
                img.save(image_path, 'JPEG', quality=95)
        except Exception as e:
            logger.error(f"Error resizing image {image_path}: {e}")

    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0 and self.available

    def get_main_image_url(self):
        """Get the main product image URL"""
        if self.image:
            return self.image.url
        return '/static/images/no-image.jpg'


class UserProfile(models.Model):
    """Extended user profile with additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address_line_1 = models.CharField(max_length=255, blank=True)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True, default='India')
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_full_address(self):
        """Return formatted full address"""
        address_parts = [
            self.address_line_1,
            self.address_line_2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ', '.join([part for part in address_parts if part])


class Order(models.Model):
    """Customer order model"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('razorpay', 'Razorpay (UPI)'),
        ('paypal', 'PayPal'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    
    # Billing Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Shipping Address
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    
    # Order details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Status and payment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_id = models.CharField(max_length=200, blank=True)  # Payment gateway transaction ID
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number}"

    def get_absolute_url(self):
        return reverse('shop:order_detail', kwargs={'order_number': self.order_number})

    def get_total_cost(self):
        """Calculate total order cost including shipping and tax"""
        return self.total_amount + self.shipping_cost + self.tax_amount

    def save(self, *args, **kwargs):
        """Generate order number if not exists"""
        if not self.order_number:
            import uuid
            self.order_number = f"FS{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price at time of purchase
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        """Calculate total cost for this item"""
        return self.price * self.quantity


class Review(models.Model):
    """Product review model"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # One review per user per product

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}/5)"


class Wishlist(models.Model):
    """User wishlist for saving favorite products"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class ShippingRate(models.Model):
    """Shipping rates based on order value or location"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, 
                                         help_text="Minimum order value for this rate")
    max_order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         help_text="Maximum order value (leave empty for unlimited)")
    cost = models.DecimalField(max_digits=10, decimal_places=2, 
                              help_text="Cost per kilogram (₹/kg)")
    min_shipping_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                             help_text="Minimum shipping charge for this country (₹)")
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                                  help_text="Order value above which shipping is free")
    country = models.CharField(max_length=100, default='India', 
                              help_text="Applicable country (India, USA, etc.)")
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Lower number = higher priority")
    
    class Meta:
        ordering = ['priority', 'min_order_value']
        
    def __str__(self):
        return f"{self.name} - {self.country} (₹{self.cost}/kg, min: ₹{self.min_shipping_charge})"
    
    @staticmethod
    def calculate_shipping_cost(cart_total, country='India', pincode=None, total_weight_kg=1.0):
        """
        Calculate shipping cost based on pincode, country lookup, and weight
        
        Flow:
        1. If pincode provided, look up country from pincode
        2. For India with pincode, use zone-based weight pricing
        3. For other countries, use country-based weight pricing (cost per kg)
        4. Fallback to default rate if no match found
        """
        # Step 1: Determine country from pincode if provided
        if pincode:
            detected_country = PincodeZone.get_country_from_pincode(pincode)
            if detected_country:
                country = detected_country
        
        # Step 2: For India, try zone-based pricing first
        if country == 'India' and pincode:
            zone_rate = ShippingZone.get_rate_for_pincode(pincode, cart_total, total_weight_kg)
            if zone_rate is not None:
                return zone_rate
        
        # Step 3: Use country-based weight pricing (cost per kg from ShippingRate)
        rates = ShippingRate.objects.filter(
            is_active=True,
            country=country,
            min_order_value__lte=cart_total
        ).order_by('priority', 'min_order_value')
        
        for rate in rates:
            # Check max order value constraint
            if rate.max_order_value and cart_total > rate.max_order_value:
                continue
            
            # Check free shipping threshold (NOT USED - no free shipping)
            # if rate.free_shipping_threshold and cart_total >= rate.free_shipping_threshold:
            #     return Decimal('0.00')
            
            # Calculate shipping cost: cost per kg × total weight
            shipping_cost = rate.cost * Decimal(str(total_weight_kg))
            
            # Apply minimum shipping charge
            if rate.min_shipping_charge and shipping_cost < rate.min_shipping_charge:
                shipping_cost = rate.min_shipping_charge
            
            return shipping_cost.quantize(Decimal('0.01'))
        
        # Step 4: Fallback - default rate per kg if no match found
        default_rate_per_kg = Decimal('50.00')
        default_min_charge = Decimal('100.00')
        shipping_cost = (default_rate_per_kg * Decimal(str(total_weight_kg))).quantize(Decimal('0.01'))
        
        # Apply default minimum charge
        if shipping_cost < default_min_charge:
            shipping_cost = default_min_charge
            
        return shipping_cost


class ShippingZone(models.Model):
    """Shipping zones for India based on regions"""
    ZONE_CHOICES = [
        ('north', 'North India'),
        ('south', 'South India'),
        ('east', 'East India'),
        ('west', 'West India'),
        ('central', 'Central India'),
    ]
    
    zone = models.CharField(max_length=20, choices=ZONE_CHOICES, unique=True)
    description = models.TextField(blank=True, help_text="States/regions covered in this zone")
    cost_per_kg = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=50.00,
        help_text="Shipping cost per kilogram for this zone"
    )
    free_shipping_threshold = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=1000.00,
        help_text="Order value above which shipping is free"
    )
    delivery_days = models.CharField(max_length=50, blank=True, help_text="Estimated delivery time")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['zone']
    
    def __str__(self):
        return f"{self.get_zone_display()} - ₹{self.cost_per_kg}/kg"
    
    @staticmethod
    def get_rate_for_pincode(pincode, cart_total, total_weight_kg):
        """Get shipping rate for a pincode based on weight"""
        try:
            pincode_obj = PincodeZone.objects.select_related('zone').get(pincode=pincode)
            if pincode_obj.zone.is_active:
                # Check free shipping threshold
                if cart_total >= pincode_obj.zone.free_shipping_threshold:
                    return Decimal('0.00')
                # Calculate shipping cost based on weight
                shipping_cost = pincode_obj.zone.cost_per_kg * Decimal(str(total_weight_kg))
                return shipping_cost.quantize(Decimal('0.01'))
        except PincodeZone.DoesNotExist:
            pass
        return None


class PincodeZone(models.Model):
    """Mapping of pincodes to shipping zones and countries"""
    pincode = models.CharField(max_length=10, unique=True, db_index=True)
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name='pincodes', null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India', help_text="Country for this pincode")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['pincode']
        indexes = [
            models.Index(fields=['pincode']),
            models.Index(fields=['country']),
        ]
    
    def __str__(self):
        if self.zone:
            return f"{self.pincode} - {self.zone.get_zone_display()} ({self.country})"
        return f"{self.pincode} - {self.country}"
    
    @staticmethod
    def get_country_from_pincode(pincode):
        """Get country from pincode/postal code"""
        try:
            pincode_obj = PincodeZone.objects.get(pincode=pincode)
            return pincode_obj.country
        except PincodeZone.DoesNotExist:
            # Return None if postal code not found - caller should use form country
            return None