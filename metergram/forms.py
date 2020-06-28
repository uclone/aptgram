from django import forms
from .models import Meter

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = [ 'dong', 'ho', 'utility', 'serial', 'mtr', 'cor', ]
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}

class DateForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['dong', 'ho', 'utility', 'serial', 'mtr', 'cor', 'amount', 'action', 'charge', 'manager']
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}