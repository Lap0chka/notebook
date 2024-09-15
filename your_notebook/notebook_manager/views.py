from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST
from notebook_manager import additional_function
from notebook_manager.forms import TitleNotebookForm, NotebookTopicForm, NotebookNoteForm, NotebookStepForm, \
    SettingsNotebookForm
from notebook_manager.models import Notebook, Note, Topic, Step


# @login_required
def create_notebook(request):
    if request.method == 'POST':
        form = TitleNotebookForm(request.POST)
        if form.is_valid():
            notebook = form.save()
            return redirect('notebook_manager:edit_notebook', notebook.slug)
    else:
        form = TitleNotebookForm()
    return render(request, 'notebooks/manager/creation/creation_notebook.html', {'form': form})


@login_required
def list_notebooks(request):
    notebooks = Notebook.objects.filter(user=request.user)
    return render(request, 'notebooks/lists/notebooks.html', {'notebooks': notebooks})


def settings_notebook(request, slug):
    notebook = get_object_or_404(Notebook, slug=slug)
    if request.method == 'POST':
        form = SettingsNotebookForm(request.POST, request.FILES, instance=notebook)
        if form.is_valid():
            form.save()
    else:
        form = SettingsNotebookForm(instance=notebook)
    context = {
        'notebook': notebook,
        'form': form
    }
    return render(
        request,
        'notebooks/manager/left_menu/notebook_settings.html',
        context
    )


@login_required
def edit_notebook(request, slug):
    topics_forms_notes = []
    notebook = get_object_or_404(Notebook, slug=slug, user=request.user)
    topics = notebook.topics.all()
    if request.method == 'POST':
        if 'note_form' in request.POST:
            additional_function.note_form(request, slug, topics)
        elif 'topic_form' in request.POST:
            additional_function.topic_form(request, slug, topics, notebook)
        elif 'delete_note' in request.POST:
            slug_note = request.POST.get('note_slug')
            additional_function.delete_note_form(request, slug_note)
        elif 'delete_topic' in request.POST:
            topic_id = request.POST.get('pk')
            additional_function.delete_topic_form(request, topic_id)
        else:
            additional_function.topic_form_update(request, slug, topics)

    topic_form = NotebookTopicForm()
    note_form = NotebookNoteForm()

    for topic in topics:
        form = NotebookTopicForm(instance=topic, initial={'pk': topic.pk})
        notes = topic.notes.all()
        topics_forms_notes.append({
            'form': form,
            'notes': notes
        })

    context = {
        'topic_form': topic_form,
        'topics_notes_forms': topics_forms_notes,
        'note_form': note_form,
        'topics': topics,
        'notebook': notebook,
    }
    return render(request, 'notebooks/manager/edit/edit_notebook.html', context)


@login_required
def edit_note(request, slug_notebook, slug_topic, slug_note, order):
    """
    View for editing a specific step of a note in a notebook.

    This function retrieves the requested note and its associated step based on the provided
    `slug` (to identify the note) and `order` (to identify the step). If the request method
    is POST, it processes the submitted form to update the note title (if changed) and the
    step content. The form is then re-rendered whether or not the form was submitted.
    """

    # Fetch the note and step, raising 404 if not found
    note = get_object_or_404(Note, slug=slug_note, user=request.user)
    step = get_object_or_404(Step, note=note, order=order)

    # Handle form submission
    if request.method == 'POST':
        form = NotebookStepForm(request.POST, instance=step)

        if form.is_valid():
            # Update the note's title only if it has been changed
            new_title = request.POST.get('note_title')
            if new_title and new_title != note.title:
                note.title = new_title
                note.save(update_fields=['title'])

            # Update the step content
            step.content = form.cleaned_data['content']
            step.save(update_fields=['content'])
            messages.success(request, 'Step was successfully updated.')

    else:
        # Instantiate the form with initial data for GET requests
        form = NotebookStepForm(instance=step)

    topics = Topic.objects.filter(user=request.user)

    # Build context for rendering
    context = {
        'note': note,
        'step': step,
        'topics': topics,
        'form': form,
    }

    # Render the template with the context
    return render(request, 'notebooks/manager/edit/edit_note.html', context)


@login_required
@require_POST
def add_step(request):
    """
    Handle POST request to add a new step to a NotebookNote.

    This function creates a new step for the given notebook note if the total
    number of steps is less than or equal to 15. If successful, it returns a JSON
    response with a redirect URL to the newly created step. If the step limit is
    exceeded, it returns an error message.
    """
    note_slug = request.POST.get('note_slug')
    note = get_object_or_404(Note, slug=note_slug, user=request.user)

    if Step.objects.filter(note=note).count() < 15:
        new_step = Step.objects.create(note=note, user=request.user)
        return JsonResponse({
            'redirect_url': reverse('notebook_manager:edit_note', args=[
                note.topic.notebook.slug,
                note.topic.slug,
                note.slug,
                new_step.order
            ])
        })
    else:
        return JsonResponse({'error': 'You have created the maximum number of steps'}, status=400)


@login_required
def delete_step(request):
    """
    Handles the deletion of a step from a notebook note.

    Expects a POST request with 'note_slug' and 'step_id' parameters.
    Deletes the step associated with the given note if it exists.

    """
    if request.method == 'POST':
        # Retrieve the note and step objects
        note = get_object_or_404(Note, slug=request.POST.get('note_slug'), user=request.user)
        step = get_object_or_404(Step, note=note, id=request.POST.get('step_id'), user=request.user)

        # Clear content for step order 1, otherwise delete the step
        if step.order == 1:
            step.content = ""
            step.save(update_fields=['content'])
        else:
            step.delete()

        # Add success message and redirect to the edit note page
        messages.success(request, 'Step deleted successfully.')
        return redirect(reverse('notebook_manager:edit_note', kwargs={
            'slug_notebook': note.topic.notebook.slug,
            'slug_topic': note.topic.slug,
            'slug_note': note.slug,
            'order': 1
        }))
