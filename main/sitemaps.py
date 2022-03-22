from django.contrib.sitemaps import Sitemap
from .models import CarAdvert, ThingsAdvert, ServicesAdvert


class CarAdvertsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return CarAdvert.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated


class ThingsAdvertsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ThingsAdvert.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated


class ServicesAdvertsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return ServicesAdvert.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated
