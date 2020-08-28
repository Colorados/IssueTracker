from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible
from django import forms
from .models import Issues


@deconstructible()
class MaxLengthValidator(BaseValidator):
    message = 'Value "%(value)s" exceeds maximum length of %(show_value)d. It should be within the limit of %(limit_value)'
    code = 'too_long'

@deconstructible()
class MinLengthValidator(BaseValidator):
    message = 'Value "%(value)s has length of %(show_value)d. It has to be at least %(limit_value) long'
    code = 'too_short'

    def compare(self, value, limit):
        return limit < value

    def clean(self, value):
        return len(value)


class IssueForm(forms.ModelForm):
    created_at = forms.DateField(required=False, label='Дата создания', input_formats=['%Y-%m-%d'],
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Issues
        fields = ['summary', 'description', 'status', 'types']


