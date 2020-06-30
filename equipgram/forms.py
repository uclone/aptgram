from django import forms
from .models import Equip
from bootstrap_datepicker_plus import DatePickerInput


class DateForm(forms.ModelForm):
    class Meta:
        model = Equip
        fields = ['code', 'subject', 'location', 'department', 'manager_1', 'manager_2', 'spec', 'date', 'remark', 'photo']
        widgets = {
            'date': DatePickerInput(format='%Y-%m-%d')
        }

        #widgets = {
        #    'date': DatePickerInput(
        #        options={
        #            "format": "YYYY-MM-DD",  # moment date-time format
        #            "showClose": True,
        #            "showClear": True,
        #            "showTodayButton": True, }, )
        #}