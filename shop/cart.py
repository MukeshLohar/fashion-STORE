"""
Shopping cart functionality using Django sessions

This module provides a session-based shopping cart that allows users
to add, update, and remove products without requiring authentication.
"""

from decimal import Decimal
from django.conf import settings
from .models import Product


class Cart:
    """Session-based shopping cart"""
    
    def __init__(self, request):
        """Initialize the cart with the current session"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID if hasattr(settings, 'CART_SESSION_ID') else 'cart')
        
        if not cart:
            # Save an empty cart in the session
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity
        
        Args:
            product: Product instance to add
            quantity: Quantity to add (default: 1)
            override_quantity: If True, replace quantity instead of adding to it
        """
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        self.save()

    def save(self):
        """Mark the session as modified to make sure it gets saved"""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, quantity):
        """Update the quantity of a product in the cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            if quantity > 0:
                self.cart[product_id]['quantity'] = quantity
                self.save()
            else:
                self.remove(product)

    def __iter__(self):
        """Iterate over the items in the cart and get the products from the database"""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        # Create a mapping of product IDs to products
        product_map = {str(product.id): product for product in products}
        
        for product_id, item in self.cart.items():
            if product_id in product_map:
                # Create a new dict without modifying session data
                yield {
                    'product': product_map[product_id],
                    'quantity': item['quantity'],
                    'price': Decimal(item['price']),
                    'total_price': Decimal(item['price']) * item['quantity']
                }

    def __len__(self):
        """Count all items in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate the total price of all items in the cart"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Remove all items from the cart"""
        del self.session['cart']
        self.save()

    def get_cart_items(self):
        """Get all cart items with product details"""
        items = []
        for item in self:
            items.append({
                'product': item['product'],
                'quantity': item['quantity'],
                'price': float(item['price']),  # Convert Decimal to float
                'total_price': float(item['total_price'])  # Convert Decimal to float
            })
        return items

    def is_empty(self):
        """Check if the cart is empty"""
        return len(self.cart) == 0

    def get_item_count(self):
        """Get total number of items (sum of quantities)"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_shipping_cost(self):
        """Calculate shipping cost based on total price"""
        total = self.get_total_price()
        if total >= Decimal('500'):  # Free shipping over ₹500
            return Decimal('0.00')
        else:
            return Decimal('50.00')  # ₹50 shipping fee

    def get_tax_amount(self):
        """Calculate tax amount (18% GST)"""
        return self.get_total_price() * Decimal('0.18')

    def get_final_total(self):
        """Get final total including shipping and tax"""
        return self.get_total_price() + self.get_shipping_cost() + self.get_tax_amount()

    def get_total_price_float(self):
        """Get total price as float for JSON serialization"""
        return float(self.get_total_price())
    
    def get_shipping_cost_float(self):
        """Get shipping cost as float for JSON serialization"""
        return float(self.get_shipping_cost())
    
    def get_tax_amount_float(self):
        """Get tax amount as float for JSON serialization"""
        return float(self.get_tax_amount())
    
    def get_final_total_float(self):
        """Get final total as float for JSON serialization"""
        return float(self.get_final_total())