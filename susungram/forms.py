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

treatment_choice= [
    ('전면', '전면'),
    ('부분', '부분'),
    ]


class SusunForm(forms.ModelForm):
    class Meta:
        model = Susun
        fields = ['category', 'subject', 'treatment', 'cycle', 'last', 'rule', 'plan', 'cost']
        widgets = {
            'category': forms.Select(choices=category_choice),
            'treatment': forms.Select(choices=treatment_choice),
        }

class DateForm(forms.ModelForm):
    class Meta:
        model = Susun
        fields = ['category', 'subject', 'treatment', 'method', 'cycle', 'ratio',
                  'last', 'rule', 'plan', 'cost', 'times', 'amount', 'file', ]
        widgets = {
            'last': DatePickerInput(format='%Y-%m-%d'),
            'rule': DatePickerInput(format='%Y-%m-%d').start_of('event days'),
            'plan': DatePickerInput(format='%Y-%m-%d').end_of('event days'),
            'category': forms.Select(choices=category_choice),
            'treatment': forms.Select(choices=treatment_choice),
        }