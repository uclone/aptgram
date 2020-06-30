from django import forms
from .models import Sulbi
from bootstrap_datepicker_plus import DatePickerInput


class DateForm(forms.ModelForm):
    class Meta:
        model = Sulbi
        fields = ['department', 'code', 'subject', 'action', 'cycle', 'start', 'close', 'text', 'file', 'remark']
        widgets = {
            'start': DatePickerInput(format='%Y-%m-%d'),
            'close': DatePickerInput(format='%Y-%m-%d'),
        }