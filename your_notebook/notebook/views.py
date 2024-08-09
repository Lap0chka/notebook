from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from notebook_manager.forms import CommentNoteForm
from notebook_manager.models import Notebook, NotebookStep, NotebookNote, Comment

from django.shortcuts import render, get_object_or_404, redirect


def index(request):
    notebooks_popular = Notebook.objects.all()[:6]
    # random notebooks
    return render(
        request, 'notebook/index.html', {'notebooks_popular': notebooks_popular}
    )


@login_required
def my_notebooks(request):
    return render(
        request, 'notebook/my_notebooks/my_notebooks.html',
    )


def notebook_page(request, slug):
    notebook = get_object_or_404(Notebook, slug=slug)
    return render(request, 'notebook/notebook_page.html', {'notebook': notebook})


def notebook_page_step(request, slug_notebook, slug_topic, slug_note, order):
    notebook = get_object_or_404(Notebook, slug=slug_notebook)
    note = get_object_or_404(NotebookNote, slug=slug_note)
    step = get_object_or_404(NotebookStep, order=order, note=note)
    comments = Comment.objects.filter(step=step, parent=None)
    steps = note.steps.all()
    steps_count = steps.count()

    context = {
        'notebook': notebook,
        'steps': steps,
        'steps_count': steps_count,
        'step': step,
        'comment_form': CommentNoteForm(),
        'comments': comments
    }

    return render(request, 'notebook/step_page.html', context)


def notebook_description(request, slug):
    notebook = get_object_or_404(Notebook, slug=slug)
    return render(request, 'notebook/description.html', {'notebook': notebook})


def notebook_reviews(request, slug):
    notebook = get_object_or_404(Notebook, slug=slug)
    return render(request, 'notebook/contact/reviews.html', {'notebook': notebook})


@login_required
def comment_step(request, slug_note, order):
    note = get_object_or_404(NotebookNote, slug=slug_note)
    step = get_object_or_404(NotebookStep, order=order, note=note)
    if request.method == 'POST':
        form = CommentNoteForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.step = step
            comment.user = request.user
            if form.cleaned_data['parent']:
                parent = form.cleaned_data['parent']
                comment.parent = parent
            comment.save()
            messages.success(request, 'Your comment has been saved')
            return redirect(step.get_absolute_url_public())

    messages.error(request, 'Something wrong try latter')
    return redirect(step.get_absolute_url_public())


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.like()
    return JsonResponse({'likes': comment.likes, 'dislikes': comment.dislikes})

@login_required
def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.dislike()
    return JsonResponse({'likes': comment.likes, 'dislikes': comment.dislikes})