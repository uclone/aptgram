from django import forms
from .models import File
from bootstrap_datepicker_plus import DatePickerInput

department_choice= [
    ('관리부', '관리부'),
    ('경리부', '경리부'),
    ('환경부', '환경부'),
    ('보안부', '보안부'),
    ]

manager_choice= [
    ('회장', '회장'),
    ('소장', '소장'),
    ('과장', '과장'),
    ('반장', '반장'),
    ]

class DateForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['department', 'charge', 'manager', 'director', 'super', 'subject', 'abstract', 'file', 'remark']
        widgets = {
            'department': forms.Select(choices=department_choice),
            'manager': forms.Select(choices=manager_choice),
        }