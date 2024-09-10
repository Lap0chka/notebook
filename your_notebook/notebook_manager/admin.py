from django.contrib import admin

from notebook_manager.models import Notebook, Note, Topic, Step, Comment


@admin.register(Notebook)
class NameNotebookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Note)
class NotebookNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Topic)
class NotebookTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Step)
class NotebookStepAdmin(admin.ModelAdmin):
    list_display = ('id', 'content',)
    readonly_fields = ('order',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
