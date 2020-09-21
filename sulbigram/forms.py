from django import forms
from .models import Sulbi
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

cycle_choice= [
    ('일간', '일간'),
    ('주간', '주간'),
    ('격주간', '격주간'),
    ('월간', '월간'),
    ('분기', '분기'),
    ('반기', '반기'),
    ('연간', '연간'),
    ]

class DateForm(forms.ModelForm):
    class Meta:
        model = Sulbi
        fields = ['department', 'code', 'subject', 'action', 'cycle', 'start', 'close', 'text', 'file', 'remark']
        widgets = {
            'start': DatePickerInput(format='%Y-%m-%d').start_of('event days'),
            'close': DatePickerInput(format='%Y-%m-%d').end_of('event days'),
            'department': forms.Select(choices=department_choice),
            'cycle': forms.Select(choices=cycle_choice),
        }

