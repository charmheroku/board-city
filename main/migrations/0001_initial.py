# Generated by Django 3.2.7 on 2021-09-12 13:19

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields
import taggit.managers
import utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarAdvert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена')),
                ('is_archive', models.BooleanField(default=False)),
                ('is_sold', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('brand', models.CharField(max_length=200, verbose_name='Марка авто')),
                ('model', models.CharField(max_length=200, verbose_name='Модель авто')),
                ('year', models.PositiveIntegerField(help_text='Введите год в формате: YYYY', validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2021)], verbose_name='Год выпуска авто')),
                ('color', models.CharField(max_length=200, verbose_name='Цвет авто')),
            ],
            options={
                'verbose_name': 'Объявление Автомобили',
                'verbose_name_plural': 'Объявления Автомобили',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Слаг')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('kod_inn', models.CharField(default='', max_length=12, validators=[utils.validate_inn], verbose_name='Код ИНН')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, default='', error_messages={'invalid': 'Введите верный номер телефона'}, max_length=128, null=True, region=None, unique=True, verbose_name='Телефон')),
                ('avatar', models.ImageField(blank=True, upload_to='avatars', verbose_name='Фото профиля')),
            ],
            options={
                'verbose_name': 'Продавец',
                'verbose_name_plural': 'Продавцы',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='ThingsAdvert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена')),
                ('is_archive', models.BooleanField(default=False)),
                ('is_sold', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('condition', models.CharField(blank=True, choices=[('new', 'Новое'), ('old', 'Б/у')], default='new', max_length=3, verbose_name='Состояние')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='main_thingsadvert', to='main.category', verbose_name='Категория')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_thingsadvert', to='main.seller', verbose_name='Продавец')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Объявление Вещи',
                'verbose_name_plural': 'Объявления Вещи',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('date_time_updated', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('сategory_subscribe', models.ManyToManyField(blank=True, related_name='subscribers', to='main.Category', verbose_name='Категории подписки')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='SMSLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_code', models.CharField(blank=True, default='', max_length=4, null=True, verbose_name='Проверочный код телефона')),
                ('response_twillio', models.TextField(blank=True, default='', null=True, verbose_name='Ответ провайдера')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='smslogs', to='main.seller', verbose_name='Продавец')),
            ],
            options={
                'verbose_name': 'Журнал Смс',
                'verbose_name_plural': 'Журналы Смс',
            },
        ),
        migrations.CreateModel(
            name='ServicesAdvert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Цена')),
                ('is_archive', models.BooleanField(default=False)),
                ('is_sold', models.BooleanField(default=False)),
                ('is_published', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('full_adress', models.CharField(max_length=255, verbose_name='Полный адрес')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='main_servicesadvert', to='main.category', verbose_name='Категория')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_servicesadvert', to='main.seller', verbose_name='Продавец')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Объявление Услуги',
                'verbose_name_plural': 'Объявления Услуги',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=80, validators=[django.core.validators.MinLengthValidator(4)], verbose_name='Название фото')),
                ('file', models.ImageField(upload_to='car_photos', verbose_name='Файл фото')),
                ('date_time_created', models.DateTimeField(auto_now_add=True)),
                ('date_time_updated', models.DateTimeField(auto_now=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='main.caradvert', verbose_name='Обьявление авто')),
            ],
            options={
                'verbose_name': 'Фото объявления',
                'verbose_name_plural': 'Фото объявления',
            },
        ),
        migrations.AddField(
            model_name='caradvert',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='main_caradvert', to='main.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='caradvert',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_caradvert', to='main.seller', verbose_name='Продавец'),
        ),
        migrations.AddField(
            model_name='caradvert',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.CreateModel(
            name='ArchiveCar',
            fields=[
            ],
            options={
                'verbose_name': 'Архив Автомобили',
                'verbose_name_plural': 'Архивы Автомобили',
                'ordering': ['-created'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.caradvert',),
        ),
        migrations.CreateModel(
            name='ArchiveServices',
            fields=[
            ],
            options={
                'verbose_name': 'Архив Услуги',
                'verbose_name_plural': 'Архивы Услуги',
                'ordering': ['-created'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.servicesadvert',),
        ),
        migrations.CreateModel(
            name='ArchiveThings',
            fields=[
            ],
            options={
                'verbose_name': 'Архив Вещи',
                'verbose_name_plural': 'Архивы Вещи',
                'ordering': ['-created'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.thingsadvert',),
        ),
    ]
