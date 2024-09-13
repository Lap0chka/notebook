
from django.urls import path

from . import views

app_name = 'notebook_manager'

urlpatterns = [
    path('create_notebook/', views.create_notebook, name='create_notebook',),
    path('settings/<slug:slug>', views.settings_notebook, name='setting_notebook',),


   # Edit note
    path('<slug:slug_notebook>/<slug:slug_topic>/<slug:slug_note>/edit_note/<int:order>', views.edit_note, name='edit_note',),
    path('edit_note/delete/', views.delete_step, name='delete_step',),
    path('add_step/', views.add_step, name='add_step',),

    #Edit notebook
    path('edit_notebook/<slug:slug>/', views.edit_notebook, name='edit_notebook',),
    path('edit_notebook/delete_note/', views.delete_note, name='delete_note',),


    path('lists/notebooks', views.list_notebooks, name='notebooks',),

]
