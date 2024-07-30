
from django.urls import path

from . import views

app_name = 'notebook'

urlpatterns = [
    path('', views.index, name='index',),
    path('my-notebooks', views.my_notebooks, name='my_notebooks',),
    path('notebook/<slug:slug>', views.notebook_page, name='notebook_page',),
    path('notebook/<slug:slug_notebook>/<slug:slug_topic>/<slug:slug_note>/<int:step_value>/', views.notebook_page_step, name='notebook_step',),

]
