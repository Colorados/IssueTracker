from django import forms
from .models import Issues


class IssueForm(forms.ModelForm):
    created_at = forms.DateField(required=False, label='Дата создания', input_formats=['%Y-%m-%d'],
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Issues
        fields = ['summary', 'description', 'status', 'types']


