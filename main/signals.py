from config import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.db.models.signals import post_save

from main.models import Category
from main.tasks import new_advert_notify


from allauth.account.signals import user_signed_up


def user_signup_receiver(request, user, **kwargs):
    """Добавление пользователей в общую группу при регистрации"""
    group, create = Group.objects.get_or_create(name="common_users")
    group.user_set.add(user)

    html_message = render_to_string("account/emails/email_welcome.html", {"user": user})

    send_mail(
        "Добро пожаловать на наш сайт!",
        strip_tags(html_message),
        settings.EMAIL_FROM,
        [user.email],
        html_message=html_message,
    )


user_signed_up.connect(user_signup_receiver, sender=User)


def advert_subcribe_receiver(sender, instance, created, **kwargs):
    """Уведомление на почту о новом объявлении по подписке"""
    if created:
        new_advert_notify(instance)


for category in Category.objects.all():
    for model in category._meta.related_objects:
        name_model = model.related_model._meta.model_name.capitalize()
        if name_model != "Subscriber":
            post_save.connect(advert_subcribe_receiver, sender=f"main.{name_model}")
