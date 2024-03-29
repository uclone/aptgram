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
        fields = ['location', 'subject', 'serial', 'mk']
        widgets = {
            'subject': forms.Select(choices=subject_choice),
        }

class ShrimpForm(forms.ModelForm):
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
        fields = ['location', 'subject', 'serial', 'temp', 'ph', 'alkali', 'salt', 'do', 'nh4', 'no2', 'turbid', 'naoh',
                  'dang', 'date', 'remark',]
        exclude = ['subject',]
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d %H:%M'),
            'subject': forms.Select(choices=subject_choice),
        }

        