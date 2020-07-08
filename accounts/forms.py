from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    email = forms.EmailField()
    last_name = forms.CharField(label='동 이름', required=True)
    first_name = forms.CharField(label='호', required=True)
    password = forms.CharField(label='패스워드', widget=forms.PasswordInput)
    password2 = forms.CharField(label='패스워드 재확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['group', 'username', 'last_name', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('패스워드가 일치하지 않습니다.')
        return cd['password2']

