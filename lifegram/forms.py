from django import forms
from .models import Life
from bootstrap_datepicker_plus import DatePickerInput


class DateForm(forms.ModelForm):
    class Meta:
        model = Life
        fields = ['contact', 'subject', 'task_1', 'photo_1', 'charge', 'department', 'task_2', 'photo_2', 'response']
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}