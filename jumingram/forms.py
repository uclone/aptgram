from django import forms
from .models import Jumin
from bootstrap_datepicker_plus import DatePickerInput


class DateForm(forms.ModelForm):
    class Meta:
        model = Jumin
        fields = ['dong', 'ho', 'represent', 'family', 'phone', 'car', 'date', 'remark', 'file']
        widgets = {
            'date': DatePickerInput(format = '%Y-%m-%d'),
        }