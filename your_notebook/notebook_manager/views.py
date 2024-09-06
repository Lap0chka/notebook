from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST

from notebook_manager.forms import TitleNotebookForm, NotebookTopicForm, NotebookNoteForm, NotebookStepForm, \
    SettingsNotebookForm
from notebook_manager.models import Notebook, NotebookNote, NotebookTopic, NotebookStep


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


# @login_required
def edit_notebook(request, slug):
    notebook = get_object_or_404(Notebook, slug=slug)
    topics = notebook.topics.all()

    if request.method == 'POST':
        topic_form = NotebookTopicForm(request.POST)

        if 'form_note' in request.POST:
            note_form = NotebookNoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                topic_id = int(request.POST.get('form_note'))
                note.topic = get_object_or_404(NotebookTopic, id=topic_id)
                note.save()
                first_step = note.steps.all().first()
                if first_step:
                    return redirect(reverse('notebook_manager:edit_note', kwargs={
                        'slug_topic': note.topic.slug, 'slug': note.slug, 'pk': first_step.pk
                    }))
                else:
                    return redirect(reverse(
                        'notebook_manager:edit_notebook',
                        kwargs={'slug': slug})
                    )
        elif topic_form.is_valid():
            instance = topic_form.save(commit=False)
            instance.notebook = notebook
            instance.save()
            return redirect(reverse(
                'notebook_manager:edit_notebook', kwargs={'slug': slug})
            )

    else:
        topic_form = NotebookTopicForm()
        note_form = NotebookNoteForm()

    context = {
        'topic_form': topic_form,
        'note_form': note_form,
        'topics': topics,
    }
    return render(request, 'notebooks/manager/edit/edit_notebook.html', context)


# @login_required
def list_notebooks(request):
    notebooks = Notebook.objects.all()
    return render(request, 'notebooks/lists/notebooks.html', {'notebooks': notebooks})


@login_required
def edit_note(request, slug_topic, slug, order):
    """
    View for editing a specific step of a note in a notebook.

    This function retrieves the requested note and its associated step based on the provided
    `slug` (to identify the note) and `order` (to identify the step). If the request method
    is POST, it processes the submitted form to update the note title (if changed) and the
    step content. The form is then re-rendered whether or not the form was submitted.
    """

    # Fetch the note and step, raising 404 if not found
    note = get_object_or_404(NotebookNote, slug=slug)
    step = get_object_or_404(NotebookStep, note=note, order=order)

    # Handle form submission
    if request.method == 'POST':
        form = NotebookStepForm(request.POST, instance=step)

        if form.is_valid():
            # Update the note's title only if it has been changed
            new_title = form.cleaned_data['title_note']
            if new_title and new_title != note.title:
                note.title = new_title
                note.save(update_fields=['title'])

            # Update the step content
            step.content = form.cleaned_data['content']
            step.save(update_fields=['content'])
            messages.success(request, 'Step was successfully updated.')

    else:
        # Instantiate the form with initial data for GET requests
        form = NotebookStepForm(instance=step, title_note=note.title)

    topics = NotebookTopic.objects.all()

    # Build context for rendering
    context = {
        'note': note,
        'step': step,
        'topics': topics,
        'form': form,
    }

    # Render the template with the context
    return render(request, 'notebooks/manager/edit/edit_note.html', context)


def add_step(request):
    """
    Handle POST request to add a new step to a NotebookNote.

    This function creates a new step for the given notebook note if the total
    number of steps is less than or equal to 15. If successful, it returns a JSON
    response with a redirect URL to the newly created step. If the step limit is
    exceeded, it returns an error message.
    """
    order = request.POST.get('order')
    note_slug = request.POST.get('note_id')
    note = get_object_or_404(NotebookNote, order=order, slug=note_slug)

    if NotebookStep.objects.filter(note=note).count() < 15:
        new_step = NotebookStep.objects.create(note=note)
        return JsonResponse({
            'redirect_url': reverse('notebook_manager:edit_note', args=[note.topic.slug, note.slug, new_step.order])
        })
    else:
        return JsonResponse({'error': 'You have created the maximum number of steps'}, status=400)


def delete_step(request):
    """
    Handles the deletion of a step from a notebook note.

    Expects a POST request with 'note_slug' and 'step_id' parameters.
    Deletes the step associated with the given note if it exists.

    """
    if request.method == 'POST':
        # Retrieve the note and step objects
        note = get_object_or_404(NotebookNote, slug=request.POST.get('note_slug'))
        step = get_object_or_404(NotebookStep, note=note, id=request.POST.get('step_id'))

        # Clear content for step order 1, otherwise delete the step
        if step.order == 1:
            step.content = ""
            step.save(update_fields=['content'])
        else:
            step.delete()

        # Add success message and redirect to the edit note page
        messages.success(request, 'Step deleted successfully.')
        return redirect(reverse('notebook_manager:edit_note', kwargs={
            'slug': note.slug,
            'slug_topic': note.topic.slug,
            'order': 1
        }))


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
        'notebooks/manager/settings/notebook_settings.html',
        context
    )
