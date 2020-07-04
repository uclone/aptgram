from django import forms
from .models import Paper
from bootstrap_datepicker_plus import DatePickerInput


class DateForm(forms.ModelForm):
    class Meta:
        model = Paper
        fields = ['subject', 'description', 'file']
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}