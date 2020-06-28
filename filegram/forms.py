from django import forms
from .models import File
from bootstrap_datepicker_plus import DatePickerInput


class DateForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['department', 'charge', 'manager', 'director', 'super', 'subject', 'abstract', 'file', 'remark']
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}