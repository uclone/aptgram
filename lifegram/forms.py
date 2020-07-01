from django import forms
from .models import Life
from bootstrap_datepicker_plus import DatePickerInput


department_choice= [
    ('관리부', '관리부'),
    ('경리부', '경리부'),
    ('환경부', '환경부'),
    ('보안부', '보안부'),
    ]

class LifeForm(forms.ModelForm):
    class Meta:
        model = Life
        fields = [ 'contact', 'subject', 'task_1', 'photo_1', ]
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}

class DateForm(forms.ModelForm):
    class Meta:
        model = Life
        fields = ['department', 'charge', 'date', 'close', 'task_2', 'photo_2', 'response']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d').start_of('event days'),
            'close': DatePickerInput(format='%Y-%m-%d').end_of('event days'),
            'department': forms.Select(choices=department_choice),
        }

