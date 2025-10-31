"""
Management command to add products with photos and inventory

Usage:
python manage.py add_product --name "Product Name" --price 99.99 --category "Category Name" --stock 10
"""

from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from decimal import Decimal
import requests
from shop.models import Product, Category


class Command(BaseCommand):
    help = 'Add a product with photo and inventory'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, required=True, help='Product name')
        parser.add_argument('--description', type=str, default='', help='Product description')
        parser.add_argument('--price', type=float, required=True, help='Product price')
        parser.add_argument('--category', type=str, required=True, help='Category name')
        parser.add_argument('--stock', type=int, default=0, help='Stock quantity')
        parser.add_argument('--size', type=str, choices=['XS', 'S', 'M', 'L', 'XL', 'XXL'], default='M', help='Size')
        parser.add_argument('--color', type=str, choices=['red', 'blue', 'green', 'black', 'white', 'yellow', 'purple', 'orange', 'pink', 'brown'], default='black', help='Color')
        parser.add_argument('--image-url', type=str, help='URL to download product image from')
        parser.add_argument('--image-path', type=str, help='Local path to product image')

    def handle(self, *args, **options):
        try:
            # Get or create category
            category, created = Category.objects.get_or_create(
                name=options['category'],
                defaults={'slug': options['category'].lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(f"Created new category: {category.name}")

            # Create product
            product = Product(
                name=options['name'],
                description=options['description'],
                price=Decimal(str(options['price'])),
                category=category,
                stock=options['stock'],
                size=options['size'],
                color=options['color'],
                available=options['stock'] > 0
            )

            # Generate slug
            base_slug = options['name'].lower().replace(' ', '-')
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            product.slug = slug

            # Handle image
            if options.get('image_url'):
                self.download_and_save_image(product, options['image_url'])
            elif options.get('image_path'):
                self.save_local_image(product, options['image_path'])

            product.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created product: {product.name} (ID: {product.id})'
                )
            )
            self.stdout.write(f'Category: {product.category.name}')
            self.stdout.write(f'Price: ₹{product.price}')
            self.stdout.write(f'Stock: {product.stock}')
            self.stdout.write(f'Available: {product.available}')
            if product.image:
                self.stdout.write(f'Image: {product.image.url}')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating product: {str(e)}')
            )

    def download_and_save_image(self, product, image_url):
        """Download image from URL and save to product"""
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            # Create a temporary file
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            
            # Save to product
            filename = f"{product.slug}.jpg"
            product.image.save(filename, File(img_temp), save=False)
            
            self.stdout.write(f"Downloaded image from: {image_url}")
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not download image: {str(e)}')
            )

    def save_local_image(self, product, image_path):
        """Save local image file to product"""
        try:
            with open(image_path, 'rb') as img_file:
                filename = f"{product.slug}.jpg"
                product.image.save(filename, File(img_file), save=False)
            
            self.stdout.write(f"Loaded image from: {image_path}")
            
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Could not load local image: {str(e)}')
            )