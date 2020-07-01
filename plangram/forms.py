from django import forms
from .models import Plan
from bootstrap_datepicker_plus import DatePickerInput

department_choice= [
    ('관리부', '관리부'),
    ('경리부', '경리부'),
    ('환경부', '환경부'),
    ('보안부', '보안부'),
    ]

class DateForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['start', 'close', 'department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'remark']
        widgets = {
            'start': DatePickerInput(format='%Y-%m-%d').start_of('event days'),
            'close': DatePickerInput(format='%Y-%m-%d').end_of('event days'),
            'department': forms.Select(choices=department_choice),
        }