from django import forms
from .models import Meter



class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = [ 'dong', 'ho', 'mtr', 'cor', 'elec', 'water', ]
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}

class DateForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['dong', 'ho', 'mtr', 'cor', 'elec', 'water', 'action', 'charge', 'manager']
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}