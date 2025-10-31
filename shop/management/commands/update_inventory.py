"""
Management command to update product inventory

Usage:
python manage.py update_inventory --product-id 1 --stock 25
python manage.py update_inventory --product-name "Blue T-Shirt" --stock 30
python manage.py update_inventory --list-products  # List all products with stock levels
"""

from django.core.management.base import BaseCommand
from shop.models import Product


class Command(BaseCommand):
    help = 'Update product inventory levels'

    def add_arguments(self, parser):
        parser.add_argument('--product-id', type=int, help='Product ID to update')
        parser.add_argument('--product-name', type=str, help='Product name to update (partial match)')
        parser.add_argument('--stock', type=int, help='New stock quantity')
        parser.add_argument('--add-stock', type=int, help='Add this amount to current stock')
        parser.add_argument('--subtract-stock', type=int, help='Subtract this amount from current stock')
        parser.add_argument('--list-products', action='store_true', help='List all products with stock levels')
        parser.add_argument('--low-stock', type=int, default=5, help='Show products with stock below this level')

    def handle(self, *args, **options):
        if options['list_products']:
            self.list_products(options['low_stock'])
            return

        if not (options['product_id'] or options['product_name']):
            self.stdout.write(
                self.style.ERROR('Please provide either --product-id or --product-name')
            )
            return

        if not any([options['stock'], options['add_stock'], options['subtract_stock']]):
            self.stdout.write(
                self.style.ERROR('Please provide --stock, --add-stock, or --subtract-stock')
            )
            return

        # Find the product
        try:
            if options['product_id']:
                product = Product.objects.get(id=options['product_id'])
            else:
                products = Product.objects.filter(name__icontains=options['product_name'])
                if products.count() == 0:
                    self.stdout.write(
                        self.style.ERROR(f'No products found matching: {options["product_name"]}')
                    )
                    return
                elif products.count() > 1:
                    self.stdout.write('Multiple products found:')
                    for p in products:
                        self.stdout.write(f'  ID: {p.id} - {p.name} (Stock: {p.stock})')
                    self.stdout.write('Please use --product-id to specify exactly which one.')
                    return
                else:
                    product = products.first()

            # Update stock
            old_stock = product.stock
            
            if options['stock'] is not None:
                product.stock = options['stock']
            elif options['add_stock']:
                product.stock += options['add_stock']
            elif options['subtract_stock']:
                product.stock = max(0, product.stock - options['subtract_stock'])
            
            # Update availability
            product.available = product.stock > 0
            product.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated {product.name}:\n'
                    f'  Old stock: {old_stock}\n'
                    f'  New stock: {product.stock}\n'
                    f'  Available: {product.available}'
                )
            )

        except Product.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Product with ID {options["product_id"]} not found')
            )

    def list_products(self, low_stock_threshold):
        """List all products with their stock levels"""
        products = Product.objects.all().order_by('category__name', 'name')
        
        self.stdout.write('=' * 80)
        self.stdout.write('INVENTORY REPORT')
        self.stdout.write('=' * 80)
        
        current_category = None
        total_products = 0
        low_stock_products = 0
        
        for product in products:
            if current_category != product.category.name:
                current_category = product.category.name
                self.stdout.write(f'\n📂 {current_category.upper()}')
                self.stdout.write('-' * 40)
            
            status = '✅' if product.available else '❌'
            stock_status = '⚠️ LOW' if product.stock <= low_stock_threshold and product.stock > 0 else ''
            if product.stock == 0:
                stock_status = '🚫 OUT'
            
            self.stdout.write(
                f'  {status} [{product.id:3d}] {product.name[:30]:<30} '
                f'Stock: {product.stock:3d} {stock_status}'
            )
            
            total_products += 1
            if product.stock <= low_stock_threshold:
                low_stock_products += 1
        
        self.stdout.write('\n' + '=' * 80)
        self.stdout.write(f'SUMMARY: {total_products} products, {low_stock_products} need restocking')
        self.stdout.write('=' * 80)