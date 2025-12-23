"""
Management command to set up international shipping rates

Usage:
python manage.py setup_international_shipping
"""

from django.core.management.base import BaseCommand
from shop.models import ShippingRate
from decimal import Decimal


class Command(BaseCommand):
    help = 'Set up international shipping rates per kilogram'

    def handle(self, *args, **options):
        self.stdout.write('Setting up international shipping rates...')
        
        # International shipping rates (per kg with minimum charges)
        shipping_rates = [
            # Asia Pacific
            {'name': 'Malaysia Standard', 'country': 'Malaysia', 'cost': Decimal('255.00'), 'min_shipping_charge': Decimal('150.00'), 'priority': 1},
            {'name': 'Singapore Standard', 'country': 'Singapore', 'cost': Decimal('290.00'), 'min_shipping_charge': Decimal('180.00'), 'priority': 1},
            {'name': 'Sri Lanka Standard', 'country': 'Sri Lanka', 'cost': Decimal('799.00'), 'min_shipping_charge': Decimal('400.00'), 'priority': 1},
            {'name': 'Maldives Standard', 'country': 'Maldives', 'cost': Decimal('343.00'), 'min_shipping_charge': Decimal('200.00'), 'priority': 1},
            {'name': 'UAE Standard', 'country': 'UAE', 'cost': Decimal('230.00'), 'min_shipping_charge': Decimal('150.00'), 'priority': 1},
            
            # Oceania
            {'name': 'Australia Standard', 'country': 'Australia', 'cost': Decimal('436.00'), 'min_shipping_charge': Decimal('250.00'), 'priority': 1},
            {'name': 'New Zealand Standard', 'country': 'New Zealand', 'cost': Decimal('649.00'), 'min_shipping_charge': Decimal('350.00'), 'priority': 1},
            
            # UK
            {'name': 'United Kingdom Standard', 'country': 'United Kingdom', 'cost': Decimal('365.00'), 'min_shipping_charge': Decimal('220.00'), 'priority': 1},
            
            # Western Europe
            {'name': 'Germany Standard', 'country': 'Germany', 'cost': Decimal('535.00'), 'min_shipping_charge': Decimal('300.00'), 'priority': 1},
            {'name': 'France Standard', 'country': 'France', 'cost': Decimal('565.00'), 'min_shipping_charge': Decimal('320.00'), 'priority': 1},
            {'name': 'Monaco Standard', 'country': 'Monaco', 'cost': Decimal('565.00'), 'min_shipping_charge': Decimal('320.00'), 'priority': 1},
            {'name': 'Austria Standard', 'country': 'Austria', 'cost': Decimal('553.00'), 'min_shipping_charge': Decimal('310.00'), 'priority': 1},
            {'name': 'Belgium Standard', 'country': 'Belgium', 'cost': Decimal('553.00'), 'min_shipping_charge': Decimal('310.00'), 'priority': 1},
            {'name': 'Luxembourg Standard', 'country': 'Luxembourg', 'cost': Decimal('553.00'), 'min_shipping_charge': Decimal('310.00'), 'priority': 1},
            {'name': 'Netherlands Standard', 'country': 'Netherlands', 'cost': Decimal('553.00'), 'min_shipping_charge': Decimal('310.00'), 'priority': 1},
            
            # Central Europe
            {'name': 'Czech Republic Standard', 'country': 'Czech Republic', 'cost': Decimal('563.00'), 'min_shipping_charge': Decimal('315.00'), 'priority': 1},
            {'name': 'Denmark Standard', 'country': 'Denmark', 'cost': Decimal('563.00'), 'min_shipping_charge': Decimal('315.00'), 'priority': 1},
            {'name': 'Hungary Standard', 'country': 'Hungary', 'cost': Decimal('576.00'), 'min_shipping_charge': Decimal('325.00'), 'priority': 1},
            {'name': 'Italy Standard', 'country': 'Italy', 'cost': Decimal('576.00'), 'min_shipping_charge': Decimal('325.00'), 'priority': 1},
            {'name': 'Poland Standard', 'country': 'Poland', 'cost': Decimal('576.00'), 'min_shipping_charge': Decimal('325.00'), 'priority': 1},
            {'name': 'Slovak Republic Standard', 'country': 'Slovak Republic', 'cost': Decimal('576.00'), 'min_shipping_charge': Decimal('325.00'), 'priority': 1},
            {'name': 'Slovenia Standard', 'country': 'Slovenia', 'cost': Decimal('576.00'), 'min_shipping_charge': Decimal('325.00'), 'priority': 1},
            {'name': 'Sweden Standard', 'country': 'Sweden', 'cost': Decimal('594.00'), 'min_shipping_charge': Decimal('335.00'), 'priority': 1},
            
            # Northern & Baltic Europe
            {'name': 'Estonia Standard', 'country': 'Estonia', 'cost': Decimal('613.00'), 'min_shipping_charge': Decimal('345.00'), 'priority': 1},
            {'name': 'Finland Standard', 'country': 'Finland', 'cost': Decimal('613.00'), 'min_shipping_charge': Decimal('345.00'), 'priority': 1},
            {'name': 'Croatia Standard', 'country': 'Croatia', 'cost': Decimal('613.00'), 'min_shipping_charge': Decimal('345.00'), 'priority': 1},
            {'name': 'Lithuania Standard', 'country': 'Lithuania', 'cost': Decimal('613.00'), 'min_shipping_charge': Decimal('345.00'), 'priority': 1},
            {'name': 'Latvia Standard', 'country': 'Latvia', 'cost': Decimal('613.00'), 'min_shipping_charge': Decimal('345.00'), 'priority': 1},
            
            # Southern & Eastern Europe
            {'name': 'Bulgaria Standard', 'country': 'Bulgaria', 'cost': Decimal('647.00'), 'min_shipping_charge': Decimal('365.00'), 'priority': 1},
            {'name': 'Bosnia Standard', 'country': 'Bosnia', 'cost': Decimal('647.00'), 'min_shipping_charge': Decimal('365.00'), 'priority': 1},
            {'name': 'Greece Standard', 'country': 'Greece', 'cost': Decimal('647.00'), 'min_shipping_charge': Decimal('365.00'), 'priority': 1},
            {'name': 'Iceland Standard', 'country': 'Iceland', 'cost': Decimal('647.00'), 'min_shipping_charge': Decimal('365.00'), 'priority': 1},
            {'name': 'Romania Standard', 'country': 'Romania', 'cost': Decimal('647.00'), 'min_shipping_charge': Decimal('365.00'), 'priority': 1},
            {'name': 'Serbia Standard', 'country': 'Serbia', 'cost': Decimal('647.00'), 'min_shipping_charge': Decimal('365.00'), 'priority': 1},
            
            # Atlantic Europe
            {'name': 'Ireland Standard', 'country': 'Ireland', 'cost': Decimal('584.00'), 'min_shipping_charge': Decimal('330.00'), 'priority': 1},
            {'name': 'Portugal Standard', 'country': 'Portugal', 'cost': Decimal('584.00'), 'min_shipping_charge': Decimal('330.00'), 'priority': 1},
        ]
        
        created_count = 0
        updated_count = 0
        
        for rate_data in shipping_rates:
            rate, created = ShippingRate.objects.update_or_create(
                name=rate_data['name'],
                country=rate_data['country'],
                defaults={
                    'description': f"Standard international shipping to {rate_data['country']} (weight-based)",
                    'cost': rate_data['cost'],
                    'min_shipping_charge': rate_data['min_shipping_charge'],
                    'min_order_value': Decimal('0.00'),
                    'max_order_value': None,
                    'free_shipping_threshold': None,  # No free shipping for international
                    'priority': rate_data['priority'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created: {rate.country} - ₹{rate.cost}/kg (min: ₹{rate.min_shipping_charge})'
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'↻ Updated: {rate.country} - ₹{rate.cost}/kg (min: ₹{rate.min_shipping_charge})'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully processed {created_count + updated_count} shipping rates!'
            )
        )
        self.stdout.write(f'  Created: {created_count}')
        self.stdout.write(f'  Updated: {updated_count}')
        
        # Display summary by region
        self.stdout.write('\n' + '='*70)
        self.stdout.write('INTERNATIONAL SHIPPING RATES SUMMARY (Per Kilogram)')
        self.stdout.write('='*70)
        
        regions = [
            ('Asia Pacific & Middle East', ['Malaysia', 'Singapore', 'Sri Lanka', 'Maldives', 'UAE']),
            ('Oceania', ['Australia', 'New Zealand']),
            ('United Kingdom', ['United Kingdom']),
            ('Western Europe (₹553/kg)', ['Germany', 'Austria', 'Belgium', 'Luxembourg', 'Netherlands']),
            ('France & Monaco (₹565/kg)', ['France', 'Monaco']),
            ('Central Europe (₹563-594/kg)', ['Czech Republic', 'Denmark', 'Hungary', 'Italy', 'Poland', 'Slovak Republic', 'Slovenia', 'Sweden']),
            ('Northern & Baltic (₹613/kg)', ['Estonia', 'Finland', 'Croatia', 'Lithuania', 'Latvia']),
            ('Southern & Eastern (₹647/kg)', ['Bulgaria', 'Bosnia', 'Greece', 'Iceland', 'Romania', 'Serbia']),
            ('Atlantic Europe (₹584/kg)', ['Ireland', 'Portugal']),
        ]
        
        for region_name, countries in regions:
            self.stdout.write(f'\n{region_name}:')
            for country in countries:
                try:
                    # Filter by active and get first (or latest) rate
                    rate = ShippingRate.objects.filter(country=country, is_active=True).order_by('-id').first()
                    if rate:
                        self.stdout.write(f'  {country:20s}: ₹{rate.cost}/kg (min: ₹{rate.min_shipping_charge})')
                except ShippingRate.DoesNotExist:
                    pass
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write('\nNOTE:')
        self.stdout.write('• All rates are per kilogram of product weight')
        self.stdout.write('• Minimum shipping charges ensure realistic costs for light packages')
        self.stdout.write('• Actual shipping = max(Weight × Rate, Minimum Charge)')
        self.stdout.write('• No free shipping for international orders')
        self.stdout.write('• Rates are in Indian Rupees (₹)')
        self.stdout.write('='*70)
