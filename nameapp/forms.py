from django import forms
from .models import KospiPredict


class NameForm(forms.ModelForm):
    class Meta:
        model = KospiPredict
        fields = ['date', 'close', 'open',]
        #widgets = {
        #    'date': DatePickerInput(format = '%Y-%m-%d'),
        #}

class DateForm(forms.ModelForm):
    class Meta:
        model = KospiPredict
        fields = ['date', 'close', 'open',]