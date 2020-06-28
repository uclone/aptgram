from django import forms
from .models import Task
from bootstrap_datepicker_plus import DatePickerInput


class DateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'response']
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}