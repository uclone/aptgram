from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy, reverse

subject_choice= [
    ('스마트가스기기', '스마트가스기기'),
    ('업무용', '업무용'),
    ]

class RegisterForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all()[1:3], label='사용목적', required=True)
    #group = forms.ModelChoiceField(queryset=Group.objects.order_by('-last_name')[:2], label='사용목적', required=True)
    email = forms.EmailField(label='이메일')
    last_name = forms.CharField(label='스마트폰번호: (-)은 생략', required=True)
    password = forms.CharField(label='패스워드(구글계정 패스워드와 동일해야 합니다.)', widget=forms.PasswordInput)
    password2 = forms.CharField(label='패스워드 재확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'group', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('패스워드가 일치하지 않습니다.')
        return cd['password2']

class UpdateForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all()[1:3], label='사용목적', required=True)
    email = forms.EmailField(label='이메일')
    last_name = forms.CharField(label='스마트폰번호: (-)은 생략', required=True)

    class Meta:
        model = User
        #fields = ['username', 'password', 'password2', 'group', 'first_name', 'last_name', 'email']
        fields = ['username', 'group', 'last_name', 'email']




