import logging
import datetime

from django.utils import timezone
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from ...models import Category, Subscriber

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


logger = logging.getLogger(__name__)


def my_job():
    # Рассылка новых объявлений за неделю по подписке
    category_related = Category.objects.first()
    for category in Category.objects.all():
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
                        "account/emails/email_week_subscribe.html", {"adverts": adverts, "category": category}
                    )
                    send_mail(
                        "Новые объявления за неделю",
                        strip_tags(html_message),
                        settings.EMAIL_FROM,
                        [
                            x.user.email
                            for x in Subscriber.objects.filter(сategory_subscribe=category)
                        ],
                        html_message=html_message,
                    )


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after our job has run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):

    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.
    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
