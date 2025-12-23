"""
Management command to set up zone-based shipping for India

Usage:
python manage.py setup_zone_shipping
"""

from django.core.management.base import BaseCommand
from shop.models import ShippingZone
from decimal import Decimal


class Command(BaseCommand):
    help = 'Set up zone-based shipping rates for India'

    def handle(self, *args, **options):
        self.stdout.write('Setting up India shipping zones...')
        
        # Clear existing zones
        ShippingZone.objects.all().delete()
        
        # Zone definitions with pricing (per kg)
        zones = [
            {
                'zone': 'north',
                'description': 'Delhi, Punjab, Haryana, Himachal Pradesh, Jammu & Kashmir, Uttarakhand, Chandigarh',
                'cost_per_kg': Decimal('40.00'),
                'free_shipping_threshold': Decimal('500.00'),
                'delivery_days': '3-5 business days',
                'is_active': True
            },
            {
                'zone': 'south',
                'description': 'Tamil Nadu, Karnataka, Kerala, Andhra Pradesh, Telangana, Puducherry',
                'cost_per_kg': Decimal('50.00'),
                'free_shipping_threshold': Decimal('500.00'),
                'delivery_days': '4-6 business days',
                'is_active': True
            },
            {
                'zone': 'east',
                'description': 'West Bengal, Odisha, Bihar, Jharkhand, Assam, Sikkim, Northeast states',
                'cost_per_kg': Decimal('60.00'),
                'free_shipping_threshold': Decimal('500.00'),
                'delivery_days': '5-7 business days',
                'is_active': True
            },
            {
                'zone': 'west',
                'description': 'Maharashtra, Gujarat, Goa, Rajasthan, Dadra & Nagar Haveli, Daman & Diu',
                'cost_per_kg': Decimal('45.00'),
                'free_shipping_threshold': Decimal('500.00'),
                'delivery_days': '3-5 business days',
                'is_active': True
            },
            {
                'zone': 'central',
                'description': 'Madhya Pradesh, Chhattisgarh, Uttar Pradesh',
                'cost_per_kg': Decimal('45.00'),
                'free_shipping_threshold': Decimal('500.00'),
                'delivery_days': '4-6 business days',
                'is_active': True
            },
        ]
        
        created_count = 0
        for zone_data in zones:
            zone = ShippingZone.objects.create(**zone_data)
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Created: {zone.get_zone_display()} - ₹{zone.cost_per_kg}/kg (Free above ₹{zone.free_shipping_threshold})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} shipping zones!'
            )
        )
        
        # Display summary
        self.stdout.write('\n' + '='*70)
        self.stdout.write('SHIPPING ZONES SUMMARY (Per Kilogram Rates)')
        self.stdout.write('='*70)
        
        for zone in ShippingZone.objects.all():
            self.stdout.write(f'\n{zone.get_zone_display().upper()}:')
            self.stdout.write(f'  Cost: ₹{zone.cost_per_kg}/kg')
            self.stdout.write(f'  Free Shipping: Above ₹{zone.free_shipping_threshold}')
            self.stdout.write(f'  Delivery: {zone.delivery_days}')
            self.stdout.write(f'  Coverage: {zone.description}')
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write('\nNEXT STEPS:')
        self.stdout.write('1. Add weight to products (in kg)')
        self.stdout.write('2. Import pincode data via Excel')
        self.stdout.write('3. Go to Admin > Pincode Zones')
        self.stdout.write('4. Click "Import from Excel"')
        self.stdout.write('5. Download sample template and fill it with pincodes')
        self.stdout.write('='*70)
