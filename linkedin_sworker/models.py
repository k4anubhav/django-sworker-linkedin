import logging
import os

from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.datetime_safe import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
SENDGRID_EMAIL_FROM = os.environ['SENDGRID_EMAIL_FROM']

logger = logging.getLogger(__name__)


class UpdateSubscription(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)
    search_links = models.ManyToManyField('SearchLink', related_name='subscriptions', blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'Update Subscriptions'
        ordering = ('-created_at',)


class SearchLink(models.Model):
    keyword = models.CharField(max_length=255, primary_key=True)
    search_link = models.URLField(validators=[
        RegexValidator(
            regex=r'^https://www\.linkedin\.com/search/results/content/\?keywords=.+',
            message='Invalid linkedin search link'
        )
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.keyword

    class Meta:
        verbose_name_plural = 'Search Keywords'
        ordering = ('-created_at',)


class LatestPost(models.Model):
    id = models.BigIntegerField(primary_key=True)
    posted_at = models.DateTimeField()
    body = models.TextField()
    search_link = models.ForeignKey(SearchLink, on_delete=models.CASCADE)

    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['posted_at']), ]
        ordering = ['-posted_at']

    def __str__(self):
        return f'{self.posted_at} - {self.body[:20]}'

    @staticmethod
    def get_posted_at(id_: int) -> datetime:
        unix_time = int(bin(id_)[2:].zfill(41)[:41], 2) / 1000
        return datetime.fromtimestamp(unix_time, tz=timezone.get_current_timezone())

    def save(self, **kwargs):
        if not self.posted_at and self.id:
            self.posted_at = self.get_posted_at(self.id)
        if self.body:
            self.body = self.body.strip()
        super().save(**kwargs)


# noinspection PyUnusedLocal
@receiver(post_save, sender=LatestPost)
def save_latest_post(sender, instance: LatestPost, **kwargs):
    latest_post = LatestPost.objects.filter(search_link_id=instance.search_link_id).first()
    # latest post not found or latest post is same as current post
    if not latest_post or latest_post.id == instance.id:
        to_emails = list(instance.search_link.subscriptions.values_list('email', flat=True))
        if not to_emails:
            logger.info(f'No subscriptions found for {instance.search_link}')
            return

        message = Mail(
            from_email=SENDGRID_EMAIL_FROM,
            to_emails=to_emails,
            subject=f'New LinkedIn post alert for {instance.search_link.keyword}',
            html_content='''
            <h1>Keyword: {keyword}</h1>
            <p>{body}</p>
            <p>Posted at: {posted_at}</p>
            '''.format(
                keyword=instance.search_link.keyword,
                body=instance.body,
                posted_at=instance.posted_at.strftime('%d %b %Y %H:%M:%S')
            )
        )
        try:
            response = sg.send(message)
            logger.info(response.status_code)
            logger.info(response.body)
            logger.info(response.headers)
        except Exception as e:
            logger.error(e, e.message if hasattr(e, 'message') else '')
