from django import forms
from .models import News
from bootstrap_datepicker_plus import DatePickerInput


class GongoForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['dong', 'ho', 'date', 'subject', 'text', 'photo', 'file']

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['dong', 'ho', 'date', 'subject', 'text', 'photo', 'file']

class DateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['dong', 'ho', 'date', 'subject', 'text', 'photo', 'file']
        widgets = {
            'date': DatePickerInput(format = '%Y-%m-%d'),
        }