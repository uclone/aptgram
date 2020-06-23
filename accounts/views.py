from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User, Group

def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            group = user_form.cleaned_data['group']
            group.user_set.add(new_user)
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()
    return render(request, 'registration/register.html', {'form':user_form})







