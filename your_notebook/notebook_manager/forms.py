from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.safestring import mark_safe

from notebook_manager.models import Notebook, Topic, Note, Step, Comment


class SettingsNotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['title', 'description', 'audience', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'st-input w-full block',
                'placeholder': 'Notebook name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'st-input w-full block',
                'rows': 6,
            }),
            'audience': forms.Textarea(attrs={
                'class': 'st-input w-full block',
                'rows': 5,
            }),
            'image': forms.FileInput(attrs={})
        }


class TitleNotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'class="ember-text-field ember-view new-course-form__input st-input'}),
        }


class NotebookTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': "ember-text-field ember-view st-input st-input-expand",
                       'placeholder': 'Topic'},
            ),
            'description': forms.Textarea(
                attrs={'class': "ember-text-field ember-view st-input st-input-expand",
                       'placeholder': 'Description',
                       'rows': 1
                       }, ),
        }


class NotebookNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'ember-text-field ember-view st-input st-size-normal st-input-expand',
                       'placeholder': 'Create note'}),
        }





class CommentNoteForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent']
        widgets = {
            'parent': forms.HiddenInput(),
            'text': forms.Textarea(
                attrs={'class': 'rich-text-editor__container '
                                'rich-text-editor__content cke_editable '
                                'cke_editable_inline cke_contents_ltr '
                                'cke_show_borders',
                       'cols': 120})
        }




class NotebookStepForm(forms.ModelForm):
    """
    A Django form for creating and updating NotebookStep instances.
    This form includes a content field

    for the step. The title field is optional.
    """

    class Meta:
        model = Step
        fields = ['content']

