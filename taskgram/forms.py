from django import forms
from .models import Task
from bootstrap_datepicker_plus import DatePickerInput

department_choice= [
    ('관리부', '관리부'),
    ('경리부', '경리부'),
    ('환경부', '환경부'),
    ('보안부', '보안부'),
    ]

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['department', 'charge', 'subject', 'task', 'photo',]
        widgets = {
            'department': forms.Select(choices=department_choice),
        }

class DateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'response']
        widgets = {
            'department': forms.Select(choices=department_choice),
        }