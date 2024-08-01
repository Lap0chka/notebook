from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NotebookNote, NotebookStep


@receiver(post_save, sender=NotebookNote)
def create_notebook_step(sender, instance, created, **kwargs):
    if created:
        NotebookStep.objects.get_or_create(note=instance)
