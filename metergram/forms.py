from django import forms
from .models import Meter

class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = [
            'dong',
            'ho',
            'serial',
            'mtr',
            'cor',
        ]