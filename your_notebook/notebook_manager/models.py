from random import sample
from string import ascii_letters, digits

from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


def rand_slug() -> str:
    """
    Generate a random slug consisting of 3 alphanumeric characters.
    """
    return "".join(sample(ascii_letters + digits, 3))


class Notebook(models.Model):
    class Mode(models.TextChoices):
        PUBLIC = 'PB', 'Public'
        PRIVATE = 'PR', 'Private'

    name = models.CharField(max_length=64)
    description = RichTextUploadingField(blank=True)
    audience = RichTextUploadingField(blank=True)
    slug = models.SlugField(max_length=76, unique=True)
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
        return reverse('notebook_manager:edit_notebook', kwargs={'slug': self.slug})

    def get_absolute_url_public(self):
        return reverse('notebook:notebook_page', kwargs={'slug': self.slug})


class NotebookTopic(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='topics')
    topic = models.CharField(max_length=128)
    slug = models.SlugField(max_length=76, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        """
        Save the category instance to the database.
        """
        if self.pk is None:
            last_step = NotebookTopic.objects.filter(notebook=self.notebook).order_by('order').last()
            self.order = last_step.order + 1 if last_step else 0
        if not self.slug:
            self.slug = slugify(rand_slug() + self.topic)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic


class NotebookNote(models.Model):
    topic = models.ForeignKey(NotebookTopic, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=76, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def get_absolute_url(self):
        first = self.steps.all().first()
        return reverse('notebook_manager:edit_note', kwargs={
            'slug_topic': self.topic.slug, 'slug': self.slug, 'pk': first.pk
        })

    def get_absolute_url_public(self):
        return reverse('notebook:notebook_step', kwargs={
            'slug_notebook': self.topic.notebook.slug,
            'slug_topic': self.topic.slug,
            'slug_note': self.slug,
            'order': 1
        })

    def save(self, *args, **kwargs):
        if self.pk is None:
            last_step = NotebookNote.objects.filter(topic=self.topic).order_by('order').last()
            self.order = last_step.order + 1 if last_step else 1
        if not self.slug:
            self.slug = slugify(rand_slug() + self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class NotebookStep(models.Model):
    note = models.ForeignKey(NotebookNote, on_delete=models.CASCADE, related_name='steps')
    content = RichTextUploadingField(blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('notebook_manager:edit_note', kwargs={
            'slug_topic': self.note.topic.slug, 'slug': self.note.slug, 'pk': self.pk
        })

    def get_absolute_url_public(self):
        return reverse('notebook:notebook_step', kwargs={
            'slug_notebook': self.note.topic.notebook.slug,
            'slug_topic': self.note.topic.slug,
            'slug_note': self.note.slug,
            'order': self.order
        })

    def save(self, *args, **kwargs):
        last_step = NotebookStep.objects.filter(note=self.note).order_by('order').last()
        self.order = last_step.order + 1 if last_step else 0
        return super().save(*args, **kwargs)


class Comment(models.Model):
    step = models.ForeignKey(NotebookStep, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-likes']

    def __str__(self):
        return f"Comment by {self.user} on {self.step.note.title} step {self.step.order}"

    def is_reply(self):
        return self.parent is not None

    def like(self):
        self.likes += 1
        self.save()

    def dislike(self):
        self.dislikes += 1
        self.save()
