"""
Management command to set up default shipping rates

Usage:
python manage.py setup_shipping
"""

from django.core.management.base import BaseCommand
from shop.models import ShippingRate
from decimal import Decimal


class Command(BaseCommand):
    help = 'Set up default shipping rates'

    def handle(self, *args, **options):
        self.stdout.write('Setting up shipping rates...')
        
        # Clear existing rates
        ShippingRate.objects.all().delete()
        
        # India Shipping Rates
        rates = [
            {
                'name': 'Standard Shipping (India)',
                'description': 'Standard delivery within 5-7 business days',
                'min_order_value': Decimal('0.00'),
                'max_order_value': Decimal('499.99'),
                'cost': Decimal('50.00'),
                'free_shipping_threshold': None,
                'country': 'India',
                'priority': 1,
                'is_active': True
            },
            {
                'name': 'Free Shipping (India)',
                'description': 'Free delivery for orders above ₹500',
                'min_order_value': Decimal('500.00'),
                'max_order_value': None,
                'cost': Decimal('0.00'),
                'free_shipping_threshold': Decimal('500.00'),
                'country': 'India',
                'priority': 0,
                'is_active': True
            },
            # USA Shipping Rates
            {
                'name': 'International Shipping (USA)',
                'description': 'International delivery within 10-15 business days',
                'min_order_value': Decimal('0.00'),
                'max_order_value': Decimal('2999.99'),
                'cost': Decimal('200.00'),
                'free_shipping_threshold': None,
                'country': 'USA',
                'priority': 1,
                'is_active': True
            },
            {
                'name': 'Free International Shipping (USA)',
                'description': 'Free international delivery for orders above ₹3000',
                'min_order_value': Decimal('3000.00'),
                'max_order_value': None,
                'cost': Decimal('0.00'),
                'free_shipping_threshold': Decimal('3000.00'),
                'country': 'USA',
                'priority': 0,
                'is_active': True
            },
            # Other Countries
            {
                'name': 'International Shipping (Others)',
                'description': 'International delivery within 10-15 business days',
                'min_order_value': Decimal('0.00'),
                'max_order_value': None,
                'cost': Decimal('250.00'),
                'free_shipping_threshold': Decimal('5000.00'),
                'country': 'Other',
                'priority': 1,
                'is_active': True
            },
        ]
        
        created_count = 0
        for rate_data in rates:
            rate = ShippingRate.objects.create(**rate_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created: {rate.name} - ₹{rate.cost}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} shipping rates!'
            )
        )
        
        # Display summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write('SHIPPING RATES SUMMARY')
        self.stdout.write('='*60)
        
        for country in ['India', 'USA', 'Other']:
            rates = ShippingRate.objects.filter(country=country, is_active=True)
            if rates.exists():
                self.stdout.write(f'\n{country}:')
                for rate in rates:
                    free_text = f' (Free above ₹{rate.free_shipping_threshold})' if rate.free_shipping_threshold else ''
                    self.stdout.write(f'  • ₹{rate.cost} for orders ₹{rate.min_order_value}+{free_text}')
