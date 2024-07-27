from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.http import require_POST

from notebook_manager.forms import TitleNotebookForm, NotebookTopicForm, NotebookNoteForm, NotebookStepForm
from notebook_manager.models import NameNotebook, NotebookNote, NotebookTopic, NotebookStep


# @login_required
def create_notebook(request):
    if request.method == 'POST':
        form = TitleNotebookForm(request.POST)
        if form.is_valid():
            notebook = form.save()
            return redirect('notebook_manager:edit_notebook', notebook.slug)
    else:
        form = TitleNotebookForm()
    return render(request, 'notebooks/manager/creation_notebook.html', {'form': form})


# @login_required
def edit_notebook(request, slug):
    name_notebook = get_object_or_404(NameNotebook, slug=slug)
    topics = name_notebook.topics.all()

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
            instance.name_notebook = name_notebook
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
    return render(request, 'notebooks/manager/edit_notebook.html', context)


# @login_required
def list_notebooks(request):
    notebooks = NameNotebook.objects.all()
    return render(request, 'notebooks/lists/notebooks.html', {'notebooks': notebooks})


def edit_note(request, slug_topic, slug, pk):
    step = get_object_or_404(NotebookStep, pk=pk)
    if request.method == 'POST':
        form = NotebookStepForm(request.POST)
        if form.is_valid():
            step = form.save(commit=False)
            step.note = get_object_or_404(NotebookNote, slug=slug)
            step.save()
        else:
            print(form.errors)
    note = get_object_or_404(NotebookNote, slug=slug)
    topics = NotebookTopic.objects.all()
    form = NotebookStepForm(instance=step)
    context = {
        'note': note,
        'topics': topics,
        'form': form,
    }
    return render(request, 'notebooks/manager/edit_note.html', context)


@require_POST
def add_step(request):
    if request.method == 'POST':
        print(request.POST)
        note_id = request.POST.get('note_id')
        note = get_object_or_404(NotebookNote, id=note_id)
        amount = len(NotebookStep.objects.all())
        if amount <= 15:
            new_step = NotebookStep.objects.create(note=note)
            new_step_id = new_step.id
            response_data = {
                'id': new_step_id,
                'message': 'Step created successfully'
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'Your created maximum steps'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
