"""
Django URL Configuration for Fashion Store

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from shop import utility_views
from shop.sitemaps import sitemaps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('accounts/', include('allauth.urls')),  # Social authentication URLs
    
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Utility endpoints
    path('.well-known/appspecific/com.chrome.devtools.json', utility_views.chrome_devtools_config, name='chrome_devtools'),
    path('robots.txt', utility_views.robots_txt, name='robots_txt'),
    path('favicon.ico', utility_views.favicon_ico, name='favicon'),
    path('apple-touch-icon.png', utility_views.apple_touch_icon, name='apple_touch_icon'),
    path('apple-touch-icon-precomposed.png', utility_views.apple_touch_icon, name='apple_touch_icon_precomposed'),
    path('manifest.json', utility_views.manifest_json, name='manifest'),
    path('.well-known/security.txt', utility_views.security_txt, name='security_txt'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)