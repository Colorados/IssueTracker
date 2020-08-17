from django import forms
from .models import Status, Type



class IssueForm(forms.Form):
    summary = forms.CharField(max_length=200, required=True, label='Краткое описание')
    description = forms.CharField(max_length=1000, required=True, label='Полное описание', widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Статус', initial='New')
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, label='Тип')
    created_at = forms.DateField(required=False,
                                 label='Дата создания',
                                 input_formats=['%Y-%m-%d'],
                                 widget=forms.DateInput(attrs={'type': 'date'}))