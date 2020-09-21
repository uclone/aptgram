from django import forms
from .models import Plan
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
        model = Plan
        fields = ['department', 'subject', 'regpsw', 'usepsw', 'remark']
        widgets = {
            'department': forms.Select(choices=department_choice),
        }

class IssueForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['author', 'regpsw', 'remark']


#class FileForm(forms.ModelForm):
#    class Meta:
#        model = Plan
#        fields = ['department', 'subject', 'regpsw' 'usepsw', 'task', 'file', 'remark']
#        widgets = {
#            'department': forms.Select(choices=department_choice),
#        }