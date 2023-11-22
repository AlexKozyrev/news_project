from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Category, Post
from django.template.loader import render_to_string
from datetime import datetime, timedelta


@shared_task
def notify_subscribers(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.postCategory.all()

    for category in categories:
        subscribers = category.subscribers.all()
        for user in subscribers:
            send_mail(
                subject=f'Новый пост в категории {category.name}',
                message=f'"{post.title}" доступен по ссылке {settings.SITE_URL}/news/{post_id}',
                from_email='from@example.com',
                recipient_list=[user.email]
            )


@shared_task
def weekly_notify():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
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

