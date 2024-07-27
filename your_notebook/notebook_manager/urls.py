
from django.urls import path

from . import views

app_name = 'notebook_manager'

urlpatterns = [
    path('create_notebook/', views.create_notebook, name='create_notebook',),
    path('edit_notebook/<slug:slug>/', views.edit_notebook, name='edit_notebook',),
    path('<slug:slug_topic>/<slug:slug>/edit_note/<int:pk>', views.edit_note, name='edit_note',),
    path('lists/notebooks', views.list_notebooks, name='notebooks',),
    path('add_step/', views.add_step, name='add_step',),
]
