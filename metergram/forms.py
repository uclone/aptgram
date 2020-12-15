from django import forms
from .models import Meter
from bootstrap_datepicker_plus import DatePickerInput

subject_choice= [
    ('스마트계량기', '스마트계량기'),
    ('스마트차단기', '스마트차단기'),
    ]

class RegistForm(forms.ModelForm):
   class Meta:
        model = Meter
        fields = ['subject', 'location', 'serial', 'mk']
        widgets = {
            'subject': forms.Select(choices=subject_choice),
        }

class CloseForm(forms.ModelForm):
   class Meta:
        model = Meter
        fields = ['location', 'serial', 'valveaction']
        exclude = ('location', 'serial', 'valveaction',)

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['subject', 'serial', 'monmtr', 'moncor', 'amtmonmtr', 'amtmoncor', 'accmtr', 'acccor',
                  'gastmp', 'gasprs', 'gasalarm',]
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'subject': forms.Select(choices=subject_choice),
        }

class ControlForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = ['subject', 'serial', 'hometmp', 'homehumid', 'homealarm', 'valveaction',]
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'subject': forms.Select(choices=subject_choice),
        }