from django import forms
from .models import Issues, Project


class IssueForm(forms.ModelForm):
    created_at = forms.DateField(required=False, label='Дата создания', input_formats=['%Y-%m-%d'],
                                 widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Issues
        fields = ['summary', 'description', 'status', 'types']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'specification', 'launch_date', 'end_date']
