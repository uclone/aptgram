from django import forms
from .models import Equip
from bootstrap_datepicker_plus import DatePickerInput

department_choice= [
    ('관리부', '관리부'),
    ('경리부', '경리부'),
    ('환경부', '환경부'),
    ('보안부', '보안부'),
    ]

class DateForm(forms.ModelForm):
    class Meta:
        model = Equip
        fields = ['code', 'subject', 'location', 'department', 'manager_1', 'manager_2', 'spec', 'date', 'remark', 'photo']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'department': forms.Select(choices=department_choice),
        }
