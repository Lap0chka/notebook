from notebook_manager.models import Notebook

from django.shortcuts import render


def index(request):
    notebooks_popular = Notebook.objects.all()[:6]
    # random notebooks
    return render(
        request, 'notebook/index.html', {'notebooks_popular': notebooks_popular}
    )
