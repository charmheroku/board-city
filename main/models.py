from datetime import datetime

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
)
from django.db import models
from django.urls import reverse
from django.conf import settings

from django.contrib.auth.models import User

from utils import validate_inn
from main.tasks import verify_phone


from taggit.managers import TaggableManager
from phonenumber_field.modelfields import PhoneNumberField


class AbstractAdvert(models.Model):

    """Абстрактная Модель обьявления"""

    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    category = models.ForeignKey(
        "Category",
        verbose_name="Категория",
        related_name="%(app_label)s_%(class)s",
        on_delete=models.PROTECT,
    )
    price = models.PositiveIntegerField(verbose_name="Цена", null=False, default=0)
    seller = models.ForeignKey(
        "Seller",
        verbose_name="Продавец",
        related_name="%(app_label)s_%(class)s",
        on_delete=models.CASCADE,
    )

    tags = TaggableManager()
    is_archive = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CarAdvert(AbstractAdvert):

    """Модель объявлений Автомобили"""

    brand = models.CharField(max_length=200, verbose_name="Марка авто")
    model = models.CharField(max_length=200, verbose_name="Модель авто")
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
        help_text="Введите год в формате: YYYY",
        verbose_name="Год выпуска авто",
    )
    color = models.CharField(max_length=200, verbose_name="Цвет авто")
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:car_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        self.title = f"{self.brand} {self.model}"
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Объявление Автомобили"
        verbose_name_plural = "Объявления Автомобили"


class ThingsAdvert(AbstractAdvert):

    """Модель объявлений Вещи"""

    NEW_CONDITION = "new"
    OLD_CONDITION = "old"
    CONDITION_CHOICES = ((NEW_CONDITION, "Новое"), (OLD_CONDITION, "Б/у"))

    condition = models.CharField(
        choices=CONDITION_CHOICES,
        max_length=3,
        blank=True,
        default=NEW_CONDITION,
        verbose_name="Состояние",
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:thing_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created"]
        verbose_name = "Объявление Вещи"
        verbose_name_plural = "Объявления Вещи"


class ServicesAdvert(AbstractAdvert):

    """Модель объявлений Услуги"""

    full_adress = models.CharField(max_length=255, verbose_name="Полный адрес")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:service_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["-created"]
        verbose_name = "Объявление Услуги"
        verbose_name_plural = "Объявления Услуги"


class ArchiveCar(CarAdvert):

    """Архив прокси модель Автомобили"""

    class Meta:
        ordering = ["-created"]
        proxy = True
        verbose_name = "Архив Автомобили"
        verbose_name_plural = "Архивы Автомобили"


class ArchiveThings(ThingsAdvert):

    """Архив прокси модель Вещи"""

    class Meta:
        ordering = ["-created"]
        proxy = True
        verbose_name = "Архив Вещи"
        verbose_name_plural = "Архивы Вещи"


class ArchiveServices(ServicesAdvert):

    """Архив прокси модель Услуги"""

    class Meta:
        ordering = ["-created"]
        proxy = True
        verbose_name = "Архив Услуги"
        verbose_name_plural = "Архивы Услуги"


class Category(models.Model):

    """Модель категорий"""

    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Слаг")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Seller(User):

    """Модель Продавца"""

    kod_inn = models.CharField(
        verbose_name="Код ИНН", max_length=12, default="", validators=[validate_inn]
    )

    phone = PhoneNumberField(
        null=True,
        verbose_name="Телефон",
        error_messages={"invalid": "Введите верный номер телефона"},
        unique=True,
        blank=True,
        default="",
    )

    avatar = models.ImageField(
        verbose_name="Фото профиля", upload_to="avatars", blank=True
    )

    def save(self, *args, **kwargs):
        if self.phone:
            verify_phone.delay(
                self.phone.as_e164,
                settings.ACCOUNT_SID,
                settings.AUTH_TOKEN,
                settings.PHONE_FROM,
                self.user_ptr_id,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)

    @property
    def adverts_total(self) -> int:

        """Кол-во объявлений продавца"""

        count_advert = self.main_caradvert.all().count()
        count_advert += self.main_thingsadvert.all().count()
        count_advert += self.main_servicesadvert.all().count()

        return count_advert

    adverts_total.fget.short_description = "Кол-во объявлений"

    class Meta:
        verbose_name = "Продавец"
        verbose_name_plural = "Продавцы"


class Tag(models.Model):

    """Модель Тегов"""

    name = models.CharField("Название", max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Picture(models.Model):

    """Модель Фото объявлений"""

    caption = models.CharField(
        verbose_name="Название фото", max_length=80, validators=[MinLengthValidator(4)]
    )
    file = models.ImageField(verbose_name="Файл фото", upload_to="car_photos")
    car = models.ForeignKey(
        "CarAdvert",
        verbose_name="Обьявление авто",
        related_name="pictures",
        on_delete=models.CASCADE,
    )
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.caption)

    class Meta:
        verbose_name = "Фото объявления"
        verbose_name_plural = "Фото объявления"


class Subscriber(models.Model):

    """Модель Подписки на объявления"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    сategory_subscribe = models.ManyToManyField(
        "Category",
        verbose_name="Категории подписки",
        related_name="subscribers",
        blank=True,
    )
    date_time_created = models.DateTimeField(auto_now_add=True)
    date_time_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class SMSLog(models.Model):

    """Модель смс логов Twillio"""

    seller = models.ForeignKey(
        "Seller",
        verbose_name="Продавец",
        related_name="smslogs",
        on_delete=models.CASCADE,
    )

    secret_code = models.CharField(
        verbose_name="Проверочный код телефона",
        max_length=4,
        blank=True,
        null=True,
        default="",
    )

    response_twillio = models.TextField(
        verbose_name="Ответ провайдера",
        blank=True,
        null=True,
        default="",
    )

    def __str__(self):
        return str(self.secret_code)

    class Meta:
        verbose_name = "Журнал Смс"
        verbose_name_plural = "Журналы Смс"
