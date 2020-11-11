from django.forms import ModelForm, DateInput
from .models import Time
from django import forms
from bootstrap_datepicker_plus import DatePickerInput

action_choice= [
    ('일정 저장', '일정 저장'),
    ('일정 삭제', '일정 삭제 (1급)'),
    ]

class TimeForm(ModelForm):
  class Meta:
    model = Time
    # datetime-local is a HTML5 input type, format to make date time show on fields

    #fields = '__all__'
    fields = ['action', 'subject', 'description', 'appendix', 'remark', 'start_time', 'end_time',]

    widgets = {
     # 'start_time': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'), #T%H:%M'),
      #'end_time': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),   #T%H:%M'),
      'start_time': DatePickerInput(format='%Y-%m-%d'),  # T%H:%M'),
      'end_time': DatePickerInput(format='%Y-%m-%d'),  # T%H:%M'),
      #'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d'),  # T%H:%M'),
      'action': forms.Select(choices=action_choice),
    }

  def __init__(self, *args, **kwargs):
    super(TimeForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%d'),   #T%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%d'),     #T%H:%M',)






