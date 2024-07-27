from django import forms

from notebook_manager.models import NameNotebook, NotebookTopic, NotebookNote, NotebookStep


class TitleNotebookForm(forms.ModelForm):
    class Meta:
        model = NameNotebook
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
