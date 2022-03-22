from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage


from .models import (
    Category,
    CarAdvert,
    ThingsAdvert,
    ServicesAdvert,
    Seller,
    Tag,
    ArchiveCar,
    ArchiveThings,
    ArchiveServices,
    Picture,
    Subscriber,
    SMSLog,
)

from ckeditor.widgets import CKEditorWidget


class FlatPageCustom(FlatPageAdmin):
    """Административная панель для простых страниц"""

    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageCustom)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Административная панель для Категорий (с автослагом)"""

    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(CarAdvert, ThingsAdvert, ServicesAdvert)
class AdvertAdmin(admin.ModelAdmin):

    list_editable = ("is_archive", "is_sold")
    ordering = ["-created"]
    actions = ["make_published", "make_archive"]
    list_display = [
        "title",
        "description",
        "category",
        "seller",
        "is_archive",
        "is_sold",
    ]

    def make_published(modeladmin, request, queryset):
        queryset.update(is_published=True)

    make_published.short_description = "Публиковать выбранные объявления"

    def make_archive(modeladmin, request, queryset):
        queryset.update(is_archive=True)

    make_archive.short_description = "Отправить в архив выбранные объявления"



@admin.register(Seller)
class SellerAdmin(UserAdmin):
    """Административная панель для профиля Продавца"""

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "kod_inn",
                    "phone",
                    "avatar",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = [
        "username",
        "kod_inn",
        "phone",
        "adverts_total",
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(ArchiveCar, ArchiveThings, ArchiveServices)
class ArchiveAdmin(admin.ModelAdmin):
    """Административная панель для Архивов объявлений"""

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_archive=True)


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    """Административная панель для Фото объявлений"""
    pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Административная панель для Подписки на рассылки"""
    pass


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    """Административная панель для логирования SMS"""
    pass
