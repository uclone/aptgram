from django import forms
from .models import Equip
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
class DateForm(forms.ModelForm):
    class Meta:
        model = Equip
        fields = ['code', 'subject', 'location', 'department', 'manager_1', 'manager_2', 'spec', 'date', 'remark', 'file']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
            'department': forms.Select(choices=department_choice),
        }
