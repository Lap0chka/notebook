from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from notebook_manager.forms import NotebookNoteForm, NotebookTopicForm
from notebook_manager.models import Note, Topic


def note_form(request, slug, topics):
    topic_id = request.POST.get('pk')
    note_form = NotebookNoteForm(request.POST)
    if note_form.is_valid():
        note = note_form.save(commit=False)
        topic = topics.get(id=topic_id)

        note.topic = topic
        note.user = request.user
        note.save()
        messages.success(request, 'Your note has been saved.')
        return redirect('notebook_manager:edit_notebook', slug)


def topic_form(request, slug, topics, notebook):
    topic_form = NotebookTopicForm(request.POST, request=request)
    if topic_form.is_valid():
        topic = topic_form.save(commit=False)
        topic.user = request.user
        topic.notebook = notebook
        topic.save()
        messages.success(request, 'Your topic has been saved.')
        return redirect('notebook_manager:edit_notebook', slug)


def topic_form_update(request, slug, topics):
    topic_id = request.POST.get('pk')
    if topic_id:
        topic = topics.get(pk=topic_id)
        topic_form = NotebookTopicForm(instance=topic, data=request.POST, request=request)
        if topic_form.is_valid():
            topic_instance = topic_form.save(commit=False)
            topic_instance.save()
            messages.success(request, 'Your topic has been updated.')
            return redirect('notebook_manager:edit_notebook', slug)



def delete_note_form(request, slug):
    try:
        note = get_object_or_404(Note, user=request.user, slug=slug)
        notebook_slug = note.notebook_object.slug
        note.delete()
        messages.success(request, 'Your note has been deleted.')
        return redirect('notebook_manager:edit_notebook', notebook_slug)
    except Exception as ex:
        messages.error(request, f'Something went wrong. {ex}')
        return redirect('notebook_manager:create_notebook')


def delete_topic_form(request, topic_id):
    try:
        topic = get_object_or_404(Topic, user=request.user, pk=topic_id)
        notebook_slug = topic.notebook.slug
        topic.delete()
        messages.success(request, 'Your topic has been deleted.')
        return redirect('notebook_manager:edit_notebook', notebook_slug)
    except Exception as ex:
        messages.error(request, f'Something went wrong. {ex}')
        return redirect('notebook_manager:create_notebook')
