from __future__ import absolute_import, unicode_literals
import datetime
import uuid

from django.utils import timezone
from config import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from main import models

from celery import shared_task
from twilio.rest import Client


@shared_task
def add(x, y):
    """Тестовая задача для Celery"""
    return x + y


@shared_task
def mul(x, y):
    """Тестовая задача для Celery"""
    return x * y


@shared_task
def new_advert_notify(instance):
    """Задача Celery для рассылки на почту о новом объявлении"""
    subscribers = list(
        models.Subscriber.objects.filter(
            сategory_subscribe=instance.category
        ).values_list("user__email", flat=True)
    )
    if subscribers:
        html_message = render_to_string(
            "account/emails/email_subscribe.html", {"advert": instance}
        )
        send_mail(
            "Новое объявление",
            strip_tags(html_message),
            settings.EMAIL_FROM,
            subscribers,
            html_message=html_message,
        )


@shared_task
def new_weekly_adverts():
    """Задача Celery для рассылки на почту о новых объявлениях за неделю"""
    category_related = models.Category.objects.first()
    for category in models.Category.objects.all():
        for model in category_related._meta.related_objects:
            name_model = model.related_model._meta.model_name.capitalize()
            if name_model != "Subscriber":
                now = timezone.now()
                start = now - datetime.timedelta(days=7)
                adverts = model.related_model.objects.filter(
                    category__name=category.name, created__gte=start
                )
                if adverts:
                    html_message = render_to_string(
                        "account/emails/email_week_subscribe.html",
                        {"adverts": adverts, "category": category},
                    )
                    send_mail(
                        "Новые объявления за неделю",
                        strip_tags(html_message),
                        settings.EMAIL_FROM,
                        [
                            x.user.email
                            for x in models.Subscriber.objects.filter(
                                сategory_subscribe=category
                            )
                        ],
                        html_message=html_message,
                    )


@shared_task
def verify_phone(phone, sid, token, from_phone, user_id):
    """Задача Celery для отправки кода на телефон"""
    secret = uuid.uuid4().hex[:4]
    phone_number = phone
    phone_from = from_phone
    account_sid = sid
    auth_token = token
    client = Client(account_sid, auth_token)
    response = client.messages.create(
        body=f"Ваш код {secret}", from_=phone_from, to=phone_number
    )
    seller = models.Seller.objects.get(id=user_id)
    models.SMSLog.objects.create(secret_code=secret, seller=seller, response_twillio=response.sid)
