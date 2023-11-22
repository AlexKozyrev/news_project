from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django_apscheduler.models import DjangoJobExecution

from NewsPaper.settings import SITE_URL
from .models import Category, Post, PostCategory
from django.template.loader import render_to_string
from datetime import datetime, timedelta, timezone


@shared_task
def notify_subscribers(post_id):
    print('hello')
    instance = Post.objects.get(pk=post_id)
    post_categories = PostCategory.objects.filter(postThrough=instance)
    categories = set(post_categories.values_list('categoryThrough__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    subject = f'Новый пост в категории {",".join(categories)}'
    text_content = (
        f'Название: {instance.title}\n'
        f'Preview: {instance.preview}\n'
        f'Link: {SITE_URL}{instance.get_absolute_url()}'
    )
    for subscriber in subscribers:
        msg = EmailMultiAlternatives(subject, text_content, None, [subscriber])
        msg.send()


@shared_task
def weekly_notify():
    print("Hello")
    last_execution = DjangoJobExecution.objects.filter(job__id='weekly_notify').last()
    today = datetime.now()
    if last_execution:
        last_execution_date = last_execution.run_etime.astimezone(timezone(settings.TIME_ZONE))
    else:
        last_execution_date = today - timedelta(weeks=1)
    posts = Post.objects.filter(dateCreation__gte=last_execution_date)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'dayly_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    if last_execution:
        last_execution.run_etime = today
        last_execution.save()
    else:
        DjangoJobExecution(job_id='weekly_notify', run_etime=today)
