from django import forms
from .models import Susun
from bootstrap_datepicker_plus import DatePickerInput

category_choice= [
    ('건물외부', '건물외부'),
    ('건물내부', '건물내부'),
    ('전기소화승강기', '전기소화승강기'),
    ('급수가스배수환기', '급수가스배수환기'),
    ('난방급탕', '난방급탕'),
    ('옥외부대복리시설', '옥외부대복리시설'),
    ]

class SusunForm(forms.ModelForm):
    class Meta:
        model = Susun
        fields = ['category', 'subject', 'treatment', 'cycle', 'last', 'rule', 'plan', 'cost']
        widgets = {
            'cycle': forms.Select(choices=category_choice),
        }

class DateForm(forms.ModelForm):
    class Meta:
        model = Susun
        fields = ['category', 'subject', 'treatment', 'method', 'cycle', 'ratio',
                  'last', 'rule', 'plan', 'cost', 'times', 'amount']
        widgets = {
            'last': DatePickerInput(format='%Y-%m-%d'),
            'rule': DatePickerInput(format='%Y-%m-%d').start_of('event days'),
            'plan': DatePickerInput(format='%Y-%m-%d').end_of('event days'),
            'cycle': forms.Select(choices=category_choice),
        }