import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from catalog.models import Product


@receiver(post_delete, sender=Product)
def delete_products(sender, instance, **kwargs):
    if instance.image_preview:
        image_path = instance.image_preview.path
        if os.path.exists(image_path):
            os.remove(image_path)
