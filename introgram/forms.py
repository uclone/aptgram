from django import forms
from .models import Intro
from bootstrap_datepicker_plus import DatePickerInput

metro_choice= [
    ('서울', '서울특별시'),
    ('부산', '부산광역시'),
    ('인천', '인천광역시'),
    ('대구', '대구광역시'),
    ('대전', '대전광역시'),
    ('광주', '광주관역시'),
    ('울산', '울산광역시'),
    ('세종', '세종자치시'),
    ('경기', '경기도'),
    ('강원', '강원도'),
    ('충북', '충청북도'),
    ('충남', '충청남도'),
    ('경북', '경상북도'),
    ('경남', '경상남도'),
    ('전북', '전라북도'),
    ('전남', '전라남도'),
    ('제주', '제주도'),
    ]

class IntroForm(forms.ModelForm):
    class Meta:
        model = Intro
        fields = ['name', 'metro', 'city', 'address', 'text', 'remark', 'view',]
        widgets = {
            'metro': forms.Select(choices=metro_choice),
        }

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Intro
        fields = ['name', 'metro', 'city', 'address', 'text', 'remark', 'photo',]
        widgets = {
            'metro': forms.Select(choices=metro_choice),
        }

class DateForm(forms.ModelForm):
    class Meta:
        model = Intro
        fields = ['name', 'metro', 'city', 'address', 'text', 'remark', 'view', 'photo']
        widgets = {
            'date': DatePickerInput(format = '%Y-%m-%d'),
            'metro': forms.Select(choices=metro_choice),
        }