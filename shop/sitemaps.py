from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from shop.models import Product, Category


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['shop:home', 'shop:product_list']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    """Sitemap for products"""
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(available=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('shop:product_detail', args=[obj.slug])


class CategorySitemap(Sitemap):
    """Sitemap for categories"""
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('shop:category_detail', args=[obj.slug])


# Dictionary of all sitemaps
sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'categories': CategorySitemap,
}