
from django.urls import path

from . import views

app_name = 'notebook'

urlpatterns = [
    path('', views.index, name='index',),
    path('my-notebooks', views.my_notebooks, name='my_notebooks',),
    path('notebook/description/<slug:slug>', views.notebook_description, name='description',),
    path('notebook/reviews/<slug:slug>', views.notebook_reviews, name='reviews',),
    path('notebook/<slug:slug>', views.notebook_page, name='notebook_page',),
    path('notebook/<slug:slug_notebook>/<slug:slug_topic>/<slug:slug_note>/<int:order>/', views.notebook_page_step, name='notebook_step',),
    # Comments
    path('notebook/comment/<slug:slug_note>/<int:order>/', views.comment_step, name='comment_step',),
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/dislike/', views.dislike_comment, name='dislike_comment'),

]
