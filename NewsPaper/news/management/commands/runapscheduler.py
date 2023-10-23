import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from news.models import Post, Category


logger = logging.getLogger(__name__)


def weekly_mailing():
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    new_posts = Post.objects.filter(
        created_at__gte=start_date, created_at__lte=end_date)
    if new_posts:
        for category in Category.objects.all():
            posts_by_category = new_posts.filter(categories=category)
            if posts_by_category:
                recipients = category.subscribers.filter(email__isnull=False)
                if recipients:
                    for recipient in recipients:
                        html_content = render_to_string(
                            'news/mailing_weekly_posts.html', {'posts': posts_by_category, \
                                'category': category, 'username': recipient.username})
                        msg = EmailMultiAlternatives(
                            subject=f"Weekly news | {category.name}",
                            body="",
                            from_email='iliab02@yandex.ru',
                            to=[recipient.email],
                        )
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()


def delete_old_job_executions(max_age=2419200):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_mailing,
            trigger=CronTrigger(day_of_week="sun", hour="20", minute="00"),
            id="weekly_mailing",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_mailing'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
