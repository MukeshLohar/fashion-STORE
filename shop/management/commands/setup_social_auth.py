"""
Management command to set up social authentication providers

This command helps configure Google and Facebook OAuth applications
for social authentication in the Django admin.
"""

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings


class Command(BaseCommand):
    help = 'Set up social authentication providers'

    def add_arguments(self, parser):
        parser.add_argument('--setup-site', action='store_true', help='Set up the default site')
        parser.add_argument('--list-apps', action='store_true', help='List configured social apps')
        parser.add_argument('--add-google', action='store_true', help='Add Google OAuth app')
        parser.add_argument('--add-facebook', action='store_true', help='Add Facebook OAuth app')
        parser.add_argument('--google-client-id', type=str, help='Google OAuth Client ID')
        parser.add_argument('--google-secret', type=str, help='Google OAuth Client Secret')
        parser.add_argument('--facebook-app-id', type=str, help='Facebook App ID')
        parser.add_argument('--facebook-secret', type=str, help='Facebook App Secret')

    def handle(self, *args, **options):
        if options['setup_site']:
            self.setup_site()
        
        if options['list_apps']:
            self.list_social_apps()
        
        if options['add_google']:
            self.add_google_app(options.get('google_client_id'), options.get('google_secret'))
        
        if options['add_facebook']:
            self.add_facebook_app(options.get('facebook_app_id'), options.get('facebook_secret'))
        
        if not any([options['setup_site'], options['list_apps'], options['add_google'], options['add_facebook']]):
            self.show_setup_instructions()

    def setup_site(self):
        """Set up the default site for allauth"""
        site, created = Site.objects.get_or_create(
            id=settings.SITE_ID,
            defaults={
                'domain': 'localhost:8000',
                'name': 'Fashion Store'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created site: {site.name} ({site.domain})'))
        else:
            # Update existing site
            site.domain = 'localhost:8000'
            site.name = 'Fashion Store'
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Updated site: {site.name} ({site.domain})'))

    def list_social_apps(self):
        """List all configured social apps"""
        apps = SocialApp.objects.all()
        
        if not apps:
            self.stdout.write(self.style.WARNING('No social apps configured yet.'))
            return
        
        self.stdout.write('\n=== CONFIGURED SOCIAL APPS ===')
        for app in apps:
            sites = ', '.join([site.domain for site in app.sites.all()])
            self.stdout.write(f'Provider: {app.provider}')
            self.stdout.write(f'Name: {app.name}')
            self.stdout.write(f'Client ID: {app.client_id}')
            self.stdout.write(f'Sites: {sites}')
            self.stdout.write('-' * 40)

    def add_google_app(self, client_id, secret):
        """Add Google OAuth app"""
        if not client_id or not secret:
            self.stdout.write(
                self.style.ERROR(
                    'Please provide both --google-client-id and --google-secret'
                )
            )
            return
        
        site = Site.objects.get(id=settings.SITE_ID)
        
        app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': secret,
            }
        )
        
        if not created:
            app.client_id = client_id
            app.secret = secret
            app.save()
        
        app.sites.add(site)
        
        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(f'{action} Google OAuth app successfully!')
        )

    def add_facebook_app(self, app_id, secret):
        """Add Facebook OAuth app"""
        if not app_id or not secret:
            self.stdout.write(
                self.style.ERROR(
                    'Please provide both --facebook-app-id and --facebook-secret'
                )
            )
            return
        
        site = Site.objects.get(id=settings.SITE_ID)
        
        app, created = SocialApp.objects.get_or_create(
            provider='facebook',
            defaults={
                'name': 'Facebook Login',
                'client_id': app_id,
                'secret': secret,
            }
        )
        
        if not created:
            app.client_id = app_id
            app.secret = secret
            app.save()
        
        app.sites.add(site)
        
        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(f'{action} Facebook app successfully!')
        )

    def show_setup_instructions(self):
        """Show setup instructions"""
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('SOCIAL AUTHENTICATION SETUP INSTRUCTIONS')
        self.stdout.write('=' * 60)
        
        self.stdout.write('\n🚀 QUICK SETUP:')
        self.stdout.write('1. Set up the default site:')
        self.stdout.write('   python manage.py setup_social_auth --setup-site')
        
        self.stdout.write('\n📋 LIST CONFIGURED APPS:')
        self.stdout.write('   python manage.py setup_social_auth --list-apps')
        
        self.stdout.write('\n🔑 GOOGLE OAUTH SETUP:')
        self.stdout.write('1. Go to: https://console.developers.google.com/')
        self.stdout.write('2. Create a new project or select existing')
        self.stdout.write('3. Enable Google+ API')
        self.stdout.write('4. Create OAuth 2.0 credentials')
        self.stdout.write('5. Add authorized redirect URI: http://localhost:8000/accounts/google/login/callback/')
        self.stdout.write('6. Run: python manage.py setup_social_auth --add-google --google-client-id YOUR_CLIENT_ID --google-secret YOUR_SECRET')
        
        self.stdout.write('\n👥 FACEBOOK LOGIN SETUP:')
        self.stdout.write('1. Go to: https://developers.facebook.com/')
        self.stdout.write('2. Create a new app')
        self.stdout.write('3. Add Facebook Login product')
        self.stdout.write('4. Add Valid OAuth Redirect URI: http://localhost:8000/accounts/facebook/login/callback/')
        self.stdout.write('5. Run: python manage.py setup_social_auth --add-facebook --facebook-app-id YOUR_APP_ID --facebook-secret YOUR_SECRET')
        
        self.stdout.write('\n🔧 MANUAL SETUP (Alternative):')
        self.stdout.write('1. Go to Django admin: http://localhost:8000/admin/')
        self.stdout.write('2. Navigate to Sites > Sites')
        self.stdout.write('3. Edit example.com to localhost:8000')
        self.stdout.write('4. Go to Social Applications > Social applications')
        self.stdout.write('5. Add your Google/Facebook app credentials')
        
        self.stdout.write('\n💡 TESTING:')
        self.stdout.write('- Visit: http://localhost:8000/login/')
        self.stdout.write('- You should see Google and Facebook login buttons')
        
        self.stdout.write('\n📱 PRODUCTION SETUP:')
        self.stdout.write('- Update Site domain to your production domain')
        self.stdout.write('- Update OAuth redirect URIs in Google/Facebook consoles')
        self.stdout.write('- Set ALLOWED_HOSTS in settings.py')
        
        self.stdout.write('\n' + '=' * 60)