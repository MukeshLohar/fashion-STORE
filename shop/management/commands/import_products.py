"""
Management command to bulk import products from CSV

CSV format should be:
name,description,price,category,stock,size,color,image_url
"T-Shirt Red","Comfortable cotton t-shirt",25.99,"Clothing",50,"M","red","https://example.com/image.jpg"
"""

import csv
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from decimal import Decimal
import requests
from shop.models import Product, Category


class Command(BaseCommand):
    help = 'Bulk import products from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')
        parser.add_argument('--skip-images', action='store_true', help='Skip downloading images')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        skip_images = options['skip_images']
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                created_count = 0
                error_count = 0
                
                for row in reader:
                    try:
                        self.create_product_from_row(row, skip_images)
                        created_count += 1
                        self.stdout.write(f"✓ Created: {row['name']}")
                    except Exception as e:
                        error_count += 1
                        self.stdout.write(
                            self.style.ERROR(f"✗ Error creating {row['name']}: {str(e)}")
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\nImport completed!\nCreated: {created_count} products\nErrors: {error_count}'
                    )
                )
                
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'CSV file not found: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error reading CSV file: {str(e)}')
            )

    def create_product_from_row(self, row, skip_images=False):
        """Create a product from CSV row data"""
        # Get or create category
        category, created = Category.objects.get_or_create(
            name=row['category'],
            defaults={'slug': row['category'].lower().replace(' ', '-')}
        )

        # Generate unique slug
        base_slug = row['name'].lower().replace(' ', '-')
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # Create product
        product = Product(
            name=row['name'],
            slug=slug,
            description=row.get('description', ''),
            price=Decimal(str(row['price'])),
            category=category,
            stock=int(row.get('stock', 0)),
            size=row.get('size', 'M'),
            color=row.get('color', 'black'),
            available=int(row.get('stock', 0)) > 0
        )

        # Handle image
        if not skip_images and row.get('image_url'):
            self.download_and_save_image(product, row['image_url'])

        product.save()
        return product

    def download_and_save_image(self, product, image_url):
        """Download image from URL and save to product"""
        try:
            response = requests.get(image_url, stream=True, timeout=10)
            response.raise_for_status()
            
            # Create a temporary file
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.content)
            img_temp.flush()
            
            # Save to product
            filename = f"{product.slug}.jpg"
            product.image.save(filename, File(img_temp), save=False)
            
        except Exception as e:
            # Don't fail the entire import for image issues
            pass