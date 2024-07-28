from django import forms
from django.utils.safestring import mark_safe

from notebook_manager.models import Notebook, NotebookTopic, NotebookNote, NotebookStep


class SettingsNotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['name', 'description', 'audience', 'image']
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
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'class="ember-text-field ember-view new-course-form__input st-input'}),
        }


class NotebookTopicForm(forms.ModelForm):
    class Meta:
        model = NotebookTopic
        fields = ['topic', 'description']
        widgets = {
            'topic': forms.TextInput(
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
        model = NotebookNote
        fields = ['title']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'ember-text-field ember-view st-input st-size-normal st-input-expand',
                       'placeholder': 'Create note'}),
        }


class NotebookStepForm(forms.ModelForm):
    class Meta:
        model = NotebookStep
        fields = ['content']
