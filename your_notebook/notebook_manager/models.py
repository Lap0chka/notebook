from random import sample
from string import ascii_letters, digits

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


def rand_slug() -> str:
    """
    Generate a random slug consisting of 3 alphanumeric characters.
    """
    return "".join(sample(ascii_letters + digits, 3))


class NameNotebook(models.Model):
    class Mode(models.TextChoices):
        PUBLIC = 'PB', 'Public'
        PRIVATE = 'PR', 'Private'

    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=76, blank=True)  # unique=True)
    image = models.ImageField(upload_to='Notebook_images/%Y/%m/', blank=True, default='default/default_notebook.jpeg')
    mode = models.CharField(
        max_length=2,
        choices=Mode.choices,
        default=Mode.PRIVATE,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Save the category instance to the database.
        """
        if not self.slug:
            self.slug = slugify(rand_slug() + self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('notebook:edit_notebook', kwargs={'slug': self.slug})


class NotebookTopic(models.Model):
    name_notebook = models.ForeignKey(NameNotebook, on_delete=models.CASCADE, related_name='topics')
    topic = models.CharField(max_length=128)
    slug = models.SlugField(max_length=76, blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        """
        Save the category instance to the database.
        """
        if not self.slug:
            self.slug = slugify(rand_slug() + self.topic)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic


class NotebookNote(models.Model):
    topic = models.ForeignKey(NotebookTopic, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=76, blank=True)

    def get_absolute_url(self):
        first = self.steps.all().first()
        return reverse('notebook:edit_note', kwargs={
            'slug_topic': self.topic.slug, 'slug': self.slug, 'pk': first.pk
        })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + self.title)
        super().save(*args, **kwargs)
        NotebookStep.objects.get_or_create(note=self)


class NotebookStep(models.Model):
    note = models.ForeignKey(NotebookNote, on_delete=models.CASCADE, related_name='steps')
    content = RichTextUploadingField(blank=True)

    def get_absolute_url(self):
        return reverse('notebook:edit_note', kwargs={
            'slug_topic': self.note.topic.slug, 'slug': self.note.slug, 'pk': self.pk
        })
