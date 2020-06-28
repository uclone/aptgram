from django import forms
from .models import Plan
from bootstrap_datepicker_plus import DatePickerInput


class DateForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['start', 'close', 'department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'remark']
        widgets = {
            'start': DatePickerInput(format='%Y-%m-%d'),
            'close': DatePickerInput(format='%Y-%m-%d'),
        }