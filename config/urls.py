from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import CarAdvertsSitemap, ThingsAdvertsSitemap, ServicesAdvertsSitemap
from main import views

sitemaps = {
    "caradverts": CarAdvertsSitemap,
    "thingsadverts": ThingsAdvertsSitemap,
    "servicesadverts": ServicesAdvertsSitemap
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("pages/", include("django.contrib.flatpages.urls")),
    path('accounts/', include('allauth.urls')),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", views.robots_txt),
    path("api/v1/adverts/", include("api.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
