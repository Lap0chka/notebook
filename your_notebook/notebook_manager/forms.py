from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.safestring import mark_safe

from notebook_manager.models import Notebook, NotebookTopic, NotebookNote, NotebookStep, Comment


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
    title_note = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'ember-text-field ember-view st-input step-editor__input lesson-edit-widget__title-input'}),
        required=False
    )

    class Meta:
        model = NotebookStep
        fields = ['content']

    def __init__(self, *args, **kwargs):
        # Extract 'title_note' from kwargs (passed during form instantiation)
        title_note_value = kwargs.pop('title_note', None)
        super(NotebookStepForm, self).__init__(*args, **kwargs)

        # Set the initial value for the 'title_note' field if it's provided
        if title_note_value:
            self.fields['title_note'].initial = title_note_value






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
