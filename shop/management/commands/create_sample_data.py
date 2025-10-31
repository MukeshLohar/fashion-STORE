"""
Django management command to create sample data for the fashion store

This command creates:
- Sample categories
- Sample products with details
- Sample users (for testing)

Usage: python manage.py create_sample_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from shop.models import Category, Product, UserProfile
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create sample data for the fashion store'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Product.objects.all().delete()
            Category.objects.all().delete()
            # Don't delete User objects to preserve admin users
            
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {
                'name': 'Women\'s Clothing',
                'description': 'Trendy clothing for women including dresses, tops, and more'
            },
            {
                'name': 'Men\'s Clothing',
                'description': 'Stylish clothing for men including shirts, pants, and accessories'
            },
            {
                'name': 'Footwear',
                'description': 'Comfortable and fashionable shoes for all occasions'
            },
            {
                'name': 'Accessories',
                'description': 'Fashion accessories including bags, belts, jewelry, and more'
            },
            {
                'name': 'Kids\' Clothing',
                'description': 'Cute and comfortable clothing for children'
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Sample products data
        products_data = [
            # Women's Clothing
            {
                'name': 'Floral Summer Dress',
                'category': 'Women\'s Clothing',
                'description': 'Beautiful floral print summer dress perfect for casual outings. Made with breathable cotton fabric.',
                'price': 1299.00,
                'stock': 25,
                'size': 'M',
                'color': 'pink',
                'material': 'Cotton',
                'brand': 'Fashion Hub'
            },
            {
                'name': 'Classic White Shirt',
                'category': 'Women\'s Clothing',
                'description': 'Elegant white shirt suitable for office wear or casual styling. Premium quality fabric.',
                'price': 899.00,
                'stock': 30,
                'size': 'L',
                'color': 'white',
                'material': 'Cotton Blend',
                'brand': 'Office Chic'
            },
            {
                'name': 'Denim Jacket',
                'category': 'Women\'s Clothing',
                'description': 'Trendy denim jacket that goes with everything. Perfect for layering.',
                'price': 1599.00,
                'stock': 20,
                'size': 'M',
                'color': 'blue',
                'material': 'Denim',
                'brand': 'Denim Co'
            },
            
            # Men's Clothing
            {
                'name': 'Formal Black Shirt',
                'category': 'Men\'s Clothing',
                'description': 'Professional black formal shirt for business meetings and special occasions.',
                'price': 1199.00,
                'stock': 35,
                'size': 'L',
                'color': 'black',
                'material': 'Cotton',
                'brand': 'Business Pro'
            },
            {
                'name': 'Casual Polo T-Shirt',
                'category': 'Men\'s Clothing',
                'description': 'Comfortable polo t-shirt for everyday wear. Available in multiple colors.',
                'price': 699.00,
                'stock': 40,
                'size': 'M',
                'color': 'navy',
                'material': 'Cotton Pique',
                'brand': 'Casual Wear'
            },
            {
                'name': 'Chino Pants',
                'category': 'Men\'s Clothing',
                'description': 'Smart casual chino pants that can be dressed up or down.',
                'price': 1399.00,
                'stock': 28,
                'size': 'L',
                'color': 'brown',
                'material': 'Cotton Twill',
                'brand': 'Smart Casuals'
            },
            
            # Footwear
            {
                'name': 'Canvas Sneakers',
                'category': 'Footwear',
                'description': 'Comfortable canvas sneakers for daily wear. Lightweight and breathable.',
                'price': 1799.00,
                'stock': 22,
                'size': 'L',
                'color': 'white',
                'material': 'Canvas',
                'brand': 'Walk Easy'
            },
            {
                'name': 'Formal Leather Shoes',
                'category': 'Footwear',
                'description': 'Classic leather formal shoes perfect for office and formal events.',
                'price': 2999.00,
                'stock': 15,
                'size': 'L',
                'color': 'black',
                'material': 'Genuine Leather',
                'brand': 'Leather Craft'
            },
            
            # Accessories
            {
                'name': 'Leather Handbag',
                'category': 'Accessories',
                'description': 'Elegant leather handbag with multiple compartments. Perfect for work or casual use.',
                'price': 2499.00,
                'stock': 18,
                'size': 'M',
                'color': 'brown',
                'material': 'Genuine Leather',
                'brand': 'Bag Studio'
            },
            {
                'name': 'Classic Watch',
                'category': 'Accessories',
                'description': 'Timeless classic watch with leather strap. Perfect accessory for any outfit.',
                'price': 3499.00,
                'stock': 12,
                'size': 'M',
                'color': 'black',
                'material': 'Steel & Leather',
                'brand': 'Time Classic'
            },
            
            # Kids' Clothing
            {
                'name': 'Kids Cotton T-Shirt',
                'category': 'Kids\' Clothing',
                'description': 'Soft and comfortable cotton t-shirt for kids. Fun prints and bright colors.',
                'price': 499.00,
                'stock': 50,
                'size': 'S',
                'color': 'red',
                'material': 'Cotton',
                'brand': 'Kids Zone'
            },
            {
                'name': 'Kids Denim Jeans',
                'category': 'Kids\' Clothing',
                'description': 'Durable denim jeans for active kids. Comfortable fit and easy to wash.',
                'price': 899.00,
                'stock': 35,
                'size': 'M',
                'color': 'blue',
                'material': 'Denim',
                'brand': 'Little Fashion'
            }
        ]
        
        # Create products
        for product_data in products_data:
            # Find the category
            category = Category.objects.get(name=product_data['category'])
            
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'slug': slugify(product_data['name']),
                    'category': category,
                    'description': product_data['description'],
                    'price': Decimal(str(product_data['price'])),
                    'stock': product_data['stock'],
                    'size': product_data['size'],
                    'color': product_data['color'],
                    'material': product_data['material'],
                    'brand': product_data['brand'],
                    'available': True,
                    'meta_description': f"{product_data['name']} - {product_data['description'][:100]}",
                    'meta_keywords': f"{product_data['name']}, {product_data['brand']}, {category.name.lower()}"
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.name}')

        # Create sample users (for testing)
        sample_users = [
            {
                'username': 'customer1',
                'email': 'customer1@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'testpass123'
            },
            {
                'username': 'customer2',
                'email': 'customer2@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'password': 'testpass123'
            }
        ]
        
        for user_data in sample_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                
                # Create user profile with sample data
                UserProfile.objects.create(
                    user=user,
                    phone=f'98765432{random.randint(10, 99)}',
                    address_line_1=f'{random.randint(1, 999)} Sample Street',
                    city='Mumbai',
                    state='Maharashtra',
                    postal_code=f'40000{random.randint(1, 9)}',
                    country='India'
                )
                
                self.stdout.write(f'Created user: {user.username}')

        # Summary
        total_categories = Category.objects.count()
        total_products = Product.objects.count()
        total_users = User.objects.count()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSample data created successfully!\n'
                f'Categories: {total_categories}\n'
                f'Products: {total_products}\n'
                f'Users: {total_users}\n\n'
                f'You can now:\n'
                f'1. Visit the website to see products\n'
                f'2. Login with sample users (customer1/customer2, password: testpass123)\n'
                f'3. Access admin panel to manage data\n'
                f'4. Test the shopping cart and checkout process'
            )
        )