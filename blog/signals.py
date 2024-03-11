import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from blog.models import Blog


@receiver(post_delete, sender=Blog)
def delete_products(sender, instance, **kwargs):
    if instance.image_preview:
        image_path = instance.image_preview.path
        if os.path.exists(image_path):
            os.remove(image_path)
