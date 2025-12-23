"""
Management command to set up international pincode mappings

Usage:
python manage.py setup_international_pincodes
"""

from django.core.management.base import BaseCommand
from shop.models import PincodeZone


class Command(BaseCommand):
    help = 'Set up international pincode to country mappings'

    def handle(self, *args, **options):
        self.stdout.write('Setting up international pincode mappings...')
        
        # Sample pincodes for different countries
        pincode_mappings = [
            # Singapore
            {'pincode': '018956', 'country': 'Singapore', 'city': 'Singapore'},
            {'pincode': '238859', 'country': 'Singapore', 'city': 'Singapore'},
            {'pincode': '629418', 'country': 'Singapore', 'city': 'Singapore'},
            
            # Malaysia
            {'pincode': '50088', 'country': 'Malaysia', 'city': 'Kuala Lumpur'},
            {'pincode': '10250', 'country': 'Malaysia', 'city': 'Penang'},
            {'pincode': '80000', 'country': 'Malaysia', 'city': 'Johor Bahru'},
            
            # UAE
            {'pincode': '00000', 'country': 'UAE', 'city': 'Dubai'},
            {'pincode': 'DXB', 'country': 'UAE', 'city': 'Dubai'},
            {'pincode': 'AUH', 'country': 'UAE', 'city': 'Abu Dhabi'},
            
            # United Kingdom
            {'pincode': 'SW1A1AA', 'country': 'United Kingdom', 'city': 'London'},
            {'pincode': 'EC1A1BB', 'country': 'United Kingdom', 'city': 'London'},
            {'pincode': 'M11AE', 'country': 'United Kingdom', 'city': 'Manchester'},
            
            # USA (ZIP codes)
            {'pincode': '10001', 'country': 'United States', 'city': 'New York'},
            {'pincode': '90001', 'country': 'United States', 'city': 'Los Angeles'},
            {'pincode': '60601', 'country': 'United States', 'city': 'Chicago'},
            
            # Australia
            {'pincode': '2000', 'country': 'Australia', 'city': 'Sydney'},
            {'pincode': '3000', 'country': 'Australia', 'city': 'Melbourne'},
            {'pincode': '4000', 'country': 'Australia', 'city': 'Brisbane'},
            
            # Canada
            {'pincode': 'M5H2N2', 'country': 'Canada', 'city': 'Toronto'},
            {'pincode': 'V6B4Y8', 'country': 'Canada', 'city': 'Vancouver'},
            
            # Germany
            {'pincode': '10115', 'country': 'Germany', 'city': 'Berlin'},
            {'pincode': '80331', 'country': 'Germany', 'city': 'Munich'},
            
            # France
            {'pincode': '75001', 'country': 'France', 'city': 'Paris'},
            {'pincode': '13001', 'country': 'France', 'city': 'Marseille'},
            
            # Sri Lanka
            {'pincode': '10100', 'country': 'Sri Lanka', 'city': 'Colombo'},
            {'pincode': '20000', 'country': 'Sri Lanka', 'city': 'Kandy'},
            
            # Maldives
            {'pincode': '20026', 'country': 'Maldives', 'city': 'Malé'},
            {'pincode': '08000', 'country': 'Maldives', 'city': 'Malé'},
        ]
        
        created_count = 0
        updated_count = 0
        
        for pincode_data in pincode_mappings:
            pincode_obj, created = PincodeZone.objects.update_or_create(
                pincode=pincode_data['pincode'],
                defaults={
                    'country': pincode_data['country'],
                    'city': pincode_data.get('city', ''),
                    'state': '',
                    'zone': None  # No zone for international pincodes
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created: {pincode_obj.pincode} → {pincode_obj.country} ({pincode_obj.city})'
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'↻ Updated: {pincode_obj.pincode} → {pincode_obj.country} ({pincode_obj.city})'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Successfully processed {created_count + updated_count} pincode mappings!'
            )
        )
        self.stdout.write(f'  Created: {created_count}')
        self.stdout.write(f'  Updated: {updated_count}')
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write('INTERNATIONAL PINCODE MAPPINGS SUMMARY')
        self.stdout.write('='*70)
        
        # Group by country
        countries = {}
        for pincode in PincodeZone.objects.filter(zone__isnull=True).order_by('country', 'pincode'):
            if pincode.country not in countries:
                countries[pincode.country] = []
            countries[pincode.country].append(f"{pincode.pincode} ({pincode.city})")
        
        for country, pincodes in sorted(countries.items()):
            self.stdout.write(f'\n{country}:')
            for pc in pincodes:
                self.stdout.write(f'  • {pc}')
        
        self.stdout.write('\n' + '='*70)
        self.stdout.write('\nNOTE:')
        self.stdout.write('• International pincodes are mapped to countries for shipping calculation')
        self.stdout.write('• Shipping cost = Weight × Country Rate (per kg)')
        self.stdout.write('• Admin can add more pincodes via Excel import in admin panel')
        self.stdout.write('='*70)
