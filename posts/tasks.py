from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import datetime

from Fanserv.Fanserv import settings
from .models import *


@shared_task
def send_notifications():
    today = datetime.datetime.now()
    after_hour = today - datetime.timedelta(hours=1)
    reply = Reply.objects.filter(status=True, time_create_post__gt=after_hour)
    authors = set(reply.all().values_list('email', flat=True))
    html_content = render_to_string(
        'reply_confirm.html',
        {
            'text': 'Your reply confirm',
            'link': settings.SITE_URL
        }
    )

    msg = EmailMultiAlternatives(
        subject='Your reply confirm',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=authors,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def posts_of_the_week():
    today = datetime.datetime.now()
    last_weak = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create_post__gt=last_weak)
    authors = set(Author.objects.all().values_list('email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Posts of the weak',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=authors,
    )

    msg.attach_alternative(html_content, 'text/html')
