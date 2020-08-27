from django import forms
from .models import Jumin
from bootstrap_datepicker_plus import DatePickerInput

class JuminForm(forms.ModelForm):
    class Meta:
        model = Jumin
        fields = ['represent', 'family', 'phone', 'car', 'date', 'remark']

class DateForm(forms.ModelForm):
    class Meta:
        model = Jumin
        fields = ['dong', 'ho', 'represent', 'family', 'phone', 'car', 'date', 'remark',]
        widgets = {
            'date': DatePickerInput(format = '%Y-%m-%d'),
        }