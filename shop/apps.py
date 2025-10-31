from django.apps import AppConfig


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    
    def ready(self):
        """Load any app initialization code here"""
        import shop.signals