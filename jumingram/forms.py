from django import forms
from .models import Jumin
from bootstrap_datepicker_plus import DatePickerInput


class GongoForm(forms.ModelForm):
    class Meta:
        model = Jumin
        fields = ['photo', 'file', 'task_apt', 'task_dong', 'task_ho', 'remark']

class JuminForm(forms.ModelForm):
    class Meta:
        model = Jumin
        fields = [ 'photo', 'file', 'task_apt', 'task_dong', 'task_ho', 'remark']

class DateForm(forms.ModelForm):
    class Meta:
        model = Jumin
        fields = ['dong', 'ho', 'represent', 'family', 'phone', 'car', 'date', 'remark',]
        widgets = {
            'date': DatePickerInput(format = '%Y-%m-%d'),
        }