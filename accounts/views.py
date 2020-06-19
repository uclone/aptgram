from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import Group

def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            #new_group = Group.objects.get(name='uclone')
            #new_user.groups.add(new_group)
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()
    return render(request, 'registration/register.html', {'form':user_form})

