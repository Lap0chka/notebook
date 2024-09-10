from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Note, Step


@receiver(post_save, sender=Note)
def create_notebook_step(sender, instance, created, **kwargs):
    if created:
        Step.objects.get_or_create(note=instance, user=instance.user)
