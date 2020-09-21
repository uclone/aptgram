from django import forms
from .models import File
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

#manager_choice= [
#    ('회장', '회장'),
#    ('소장', '소장'),
#    ('과장', '과장'),
#    ('반장', '반장'),
#    ]

class DateForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['department', 'subject', 'abstract', 'file', 'approval', 'charge', 'manager', 'director', 'board', 'super', 'visor']
        widgets = {
            'department': forms.Select(choices=department_choice),
            #'manager': forms.Select(choices=manager_choice),
        }