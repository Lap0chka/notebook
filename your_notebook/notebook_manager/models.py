from random import sample
from string import ascii_letters, digits

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.template.context_processors import request
from django.template.defaultfilters import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


def rand_slug() -> str:
    """
    Generate a random slug consisting of 3 alphanumeric characters.
    """
    return "".join(sample(ascii_letters + digits, 3))


class TitleSlugMixin(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CommonFieldsNotebook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order']

    def get_filter_params(self):
        return

    def save(self, *args, **kwargs):
        """
        Save the category instance to the database.
        """
        if self.pk is None:
            last_step = self.__class__.objects.filter(user=self.user, **self.get_filter_params()).order_by(
                'order').last()
            self.order = last_step.order + 1 if last_step else 1
        super().save(*args, **kwargs)


class Notebook(TitleSlugMixin):
    class Mode(models.TextChoices):
        PUBLIC = 'PB', 'Public'
        PRIVATE = 'PR', 'Private'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = RichTextUploadingField(blank=True)
    audience = RichTextUploadingField(blank=True)
    image = models.ImageField(upload_to='Notebook_images/%Y/%m/', blank=True, default='default/default_notebook.jpeg')
    mode = models.CharField(
        max_length=2,
        choices=Mode.choices,
        default=Mode.PRIVATE,
    )

    def get_absolute_url(self):
        return reverse('notebook_manager:edit_notebook', kwargs={'slug': self.slug})

    def get_absolute_url_public(self):
        return reverse('notebook:notebook_page', kwargs={'slug': self.slug})


class Topic(TitleSlugMixin, CommonFieldsNotebook):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='topics')
    description = models.TextField(blank=True)

    def get_filter_params(self):
        return {'notebook': self.notebook}


class Note(TitleSlugMixin, CommonFieldsNotebook):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='notes')

    def get_filter_params(self):
        return {'topic': self.topic}

    def get_url_kwargs(self):
        return {
            'slug_notebook': self.topic.notebook.slug,
            'slug_topic': self.topic.slug,
            'slug_note': self.slug,
            'order': 1
        }

    def get_absolute_url(self):
        return reverse('notebook_manager:edit_note', kwargs=self.get_url_kwargs())

    def get_absolute_url_public(self):
        return reverse('notebook:notebook_step', kwargs=self.get_url_kwargs())

    @property
    def notebook_object(self):
        return self.topic.notebook


class Step(CommonFieldsNotebook):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='steps')
    content = RichTextUploadingField(blank=True)


    def get_url_kwargs(self):
        return {
            'slug_notebook': self.note.topic.notebook.slug,
            'slug_topic': self.note.topic.slug,
            'slug_note': self.note.slug,
            'order': self.order
        }

    def get_absolute_url(self):
        return reverse('notebook_manager:edit_note', kwargs=self.get_url_kwargs())

    def get_absolute_url_public(self):
        return reverse('notebook:notebook_step', self.get_url_kwargs())

    def get_filter_params(self):
        return {'note': self.note}


class Comment(models.Model):
    step = models.ForeignKey(Step, on_delete=models.CASCADE, related_name='comments')
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
