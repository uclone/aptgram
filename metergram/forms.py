from django import forms
from .models import Meter
from bootstrap_datepicker_plus import DatePickerInput

subject_choice= [
    ('측정장치', '측정장치'),
    ('조작장치', '조작장치'),
    ]

class RegistForm(forms.ModelForm):
   class Meta:
        model = Meter
        fields = ['location', 'subject', 'serial']
        widgets = {
            'subject': forms.Select(choices=subject_choice),
        }

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['serial', 'mtr', 'cor', 'elec', 'water', 'temp', 'humidity', 'usegas', 'usewater', 'alarm', 'date']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'subject': forms.Select(choices=subject_choice),
        }

class ControlForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['location', 'subject', 'serial', 'actgas', 'actalarm', 'remark', ]
        widgets = {
            #'date': DatePickerInput(format='%Y-%m-%d'),
            'subject': forms.Select(choices=subject_choice),
        }