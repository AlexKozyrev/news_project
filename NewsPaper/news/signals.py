from django.contrib.admin import action
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from .models import Post
from .tasks import notify_subscribers


@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        notify_subscribers.delay(instance.id)