"""
Utility views for handling special requests
"""
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
@require_http_methods(["GET"])
def chrome_devtools_config(request):
    """
    Handle Chrome DevTools configuration requests
    Returns an empty JSON response to prevent 404 errors
    """
    return JsonResponse({
        "devtools": {
            "support": False,
            "message": "DevTools debugging not enabled for this application"
        }
    })


@csrf_exempt
@require_http_methods(["GET"])
def robots_txt(request):
    """
    Handle robots.txt requests
    """
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /cart/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@csrf_exempt
@require_http_methods(["GET"])
def favicon_ico(request):
    """
    Handle favicon.ico requests
    Returns a 204 No Content response if no favicon is available
    """
    return HttpResponse(status=204)


@csrf_exempt
@require_http_methods(["GET"])
def apple_touch_icon(request):
    """
    Handle apple-touch-icon requests
    Returns a 204 No Content response if no icon is available
    """
    return HttpResponse(status=204)


@csrf_exempt
@require_http_methods(["GET"])
def manifest_json(request):
    """
    Handle manifest.json requests for PWA
    """
    manifest = {
        "name": "Sri Devi Fashion Jewellery",
        "short_name": "Sri Devi Fashion Jewellery",
        "description": "Premium Fashion E-commerce Store",
        "start_url": "/",
        "display": "standalone",
        "theme_color": "#1a1a1a",
        "background_color": "#ffffff",
        "icons": [
            {
                "src": "/static/icons/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "/static/icons/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }
    return JsonResponse(manifest)


@csrf_exempt
@require_http_methods(["GET"])
def security_txt(request):
    """
    Handle security.txt requests
    """
    lines = [
        "Contact: mailto:security@fashionstore.com",
        "Expires: 2026-12-31T23:59:59.000Z",
        "Preferred-Languages: en",
        "Canonical: https://fashionstore.com/.well-known/security.txt"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")