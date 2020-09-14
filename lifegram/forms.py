from django import forms
from .models import Life
from bootstrap_datepicker_plus import DatePickerInput


department_choice= [
    ('관리부', '관리부'),
    ('경리부', '경리부'),
    ('설비부', '설비부'),
    ('전기부', '전기부'),
    ('영선부', '영선부'),
    ('조겅부', '조경부'),
    ('환경부', '환경부'),
    ('경비부', '경비부'),
    ]

class LifeForm(forms.ModelForm):
    class Meta:
        model = Life
        fields = [ 'applicant', 'subject', 'task_1', 'photo_1', 'response', ]
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Life
        fields = ['subject', 'department', 'charge', 'date', 'close', 'progress', 'task_2', 'photo_2',]
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}

class DateForm(forms.ModelForm):
    class Meta:
        model = Life
        fields = ['subject', 'department', 'charge', 'date', 'close', 'progress', 'task_2', 'photo_2',]
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d').start_of('event days'),
            'close': DatePickerInput(format='%Y-%m-%d').end_of('event days'),
            'department': forms.Select(choices=department_choice),
        }

