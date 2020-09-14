from django import forms
from .models import News
from bootstrap_datepicker_plus import DatePickerInput


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['dong', 'ho', 'date', 'subject', 'text', 'remark', 'file']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['dong', 'ho', 'date', 'subject', 'text', 'remark', 'photo']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d'),
        }

class DateForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['dong', 'ho', 'date', 'subject', 'text', 'remark', 'file', 'photo']
        widgets = {
            'date': DatePickerInput(format = '%Y-%m-%d'),
        }