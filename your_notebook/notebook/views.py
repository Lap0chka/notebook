from django.contrib.auth.decorators import login_required

from notebook_manager.models import Notebook, NotebookStep, NotebookNote

from django.shortcuts import render, get_object_or_404


def index(request):
    notebooks_popular = Notebook.objects.all()[:6]
    # random notebooks
    return render(
        request, 'notebook/index.html', {'notebooks_popular': notebooks_popular}
    )


@login_required
def my_notebooks(request):
    return render(
        request, 'notebook/my_notebooks.html',
    )


def notebook_page(request, slug):
    notebook = get_object_or_404(Notebook, slug=slug)
    return render(request, 'notebook/notebook_page.html', {'notebook': notebook})


def notebook_page_step(request, slug_notebook, slug_topic, slug_note, step_value):
    notebook = get_object_or_404(Notebook, slug=slug_notebook)
    note = get_object_or_404(NotebookNote, slug=slug_note)
    step = get_object_or_404(NotebookStep, value=step_value, note=note)

    steps = note.steps.all()
    steps_count = steps.count()

    context = {
        'notebook': notebook,
        'steps': steps,
        'steps_count': steps_count,
        'step': step
    }

    return render(request, 'notebook/step_page.html', context)


def notebook_description(request, slug):
    notebook = get_object_or_404(Notebook, slug=slug)
    return render(request, 'notebook/description.html', {'notebook': notebook})
