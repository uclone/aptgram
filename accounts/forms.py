from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    email = forms.EmailField()
    password = forms.CharField(label='패스워드', widget=forms.PasswordInput)
    password2 = forms.CharField(label='패스워드 재확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['group', 'username', 'first_name', 'last_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('패스워드가 일치하지 않습니다.')
        return cd['password2']

