from django.contrib import admin

from notebook_manager.models import Notebook, NotebookNote, NotebookTopic, NotebookStep


@admin.register(Notebook)
class NameNotebookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(NotebookNote)
class NotebookNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(NotebookTopic)
class NotebookTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic',)
    prepopulated_fields = {"slug": ("topic",)}


@admin.register(NotebookStep)
class NotebookStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'content',)
    readonly_fields = ('order',)

