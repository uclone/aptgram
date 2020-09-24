from django import forms
from .models import Poll, Choice
from bootstrap_datepicker_plus import DatePickerInput


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['subject', 'pub_date', 'open_date', 'close_date', 'remark']
        widgets = {
            'pub_date': DatePickerInput(format='%Y-%m-%d'),
            'open_date': DatePickerInput(format='%Y-%m-%d'),
            'close_date': DatePickerInput(format='%Y-%m-%d'),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['selection']
        exclude = ('poll',)