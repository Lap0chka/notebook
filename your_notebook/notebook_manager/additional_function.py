from django.contrib import messages
from django.shortcuts import redirect

from notebook_manager.forms import NotebookNoteForm, NotebookTopicForm



def note_form(request, slug, topics):
    topic_id = request.POST.get('pk')
    note_form = NotebookNoteForm(request.POST)
    if note_form.is_valid():
        note = note_form.save(commit=False)
        topic = topics.get(id=topic_id)
        if topic.notes.filter(title=note.title).exists():
            messages.error(request, 'This name already exists, try another')
            return redirect('notebook_manager:edit_notebook', slug)
        note.topic = topic
        note.user = request.user
        note.save()
        messages.success(request, 'Your note has been saved.')
        return redirect('notebook_manager:edit_notebook', slug)


def topic_form(request, slug, topics, notebook):
    topic_form = NotebookTopicForm(request.POST)
    if topic_form.is_valid():
        topic = topic_form.save(commit=False)
        if topics.filter(title=topic.title).exists():
            messages.error(request, 'This name already exists, try another')
            return redirect('notebook_manager:edit_notebook', slug)
        topic.user = request.user
        topic.notebook = notebook
        topic.save()
        messages.success(request, 'Your topic has been saved.')
        return redirect('notebook_manager:edit_notebook', slug)

def topic_form_update(request, slug, topics):
    topic_id = request.POST.get('pk')
    if topic_id:
        topic = topics.get(pk=topic_id)
        topic_form = NotebookTopicForm(instance=topic, data=request.POST)
        if topic_form.is_valid():
            topic_instance = topic_form.save(commit=False)
            if topics.filter(title=topic_instance.title).exists() and topic.title == topic_instance.title:
                messages.error(request, 'This name already exists, try another')
                return redirect('notebook_manager:edit_notebook', slug)
            topic_instance.save()
            messages.success(request, 'Your topic has been updated.')
            return redirect('notebook_manager:edit_notebook', slug)