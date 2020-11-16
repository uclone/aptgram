from django import forms
from .models import Shrimp
from bootstrap_datepicker_plus import DatePickerInput

subject_choice= [
    ('측정장치', '측정장치'),
    ('조작장치', '조작장치'),
    ]

class RegistForm(forms.ModelForm):
    class Meta:
        model = Shrimp
        fields = ['location', 'subject', 'serial']
        widgets = {
            'subject': forms.Select(choices=subject_choice),
        }

class MeterForm(forms.ModelForm):
    class Meta:
        model = Shrimp
        fields = ['serial', 'temp', 'ph', 'alkali', 'salt', 'do', 'nh4', 'no2', 'turbid', 'security', 'date']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'subject': forms.Select(choices=subject_choice),
        }

class ControlForm(forms.ModelForm):
    class Meta:
        model = Shrimp
        fields = ['location', 'subject', 'serial', 'naoh', 'dang', 'blower', 'boiler', 'remark',]
        widgets = {
            #'date': DatePickerInput(format='%Y-%m-%d'),
            'subject': forms.Select(choices=subject_choice),
        }

        