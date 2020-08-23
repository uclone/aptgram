from django import forms
from .models import Susun
from bootstrap_datepicker_plus import DatePickerInput


class SusunForm(forms.ModelForm):
    class Meta:
        model = Susun
        fields = ['category', 'subject', 'treatment', 'cycle', 'last', 'rule', 'plan', 'cost']
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}

class DateForm(forms.ModelForm):
    class Meta:
        model = Susun
        fields = ['category', 'subject', 'treatment', 'method', 'cycle', 'ratio',
                  'last', 'rule', 'plan', 'cost', 'times', 'amount']
        widgets = {
            'last': DatePickerInput(format='%Y-%m-%d'),
            'rule': DatePickerInput(format='%Y-%m-%d').start_of('event days'),
            'plan': DatePickerInput(format='%Y-%m-%d').end_of('event days')
        }