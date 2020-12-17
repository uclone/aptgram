from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
from shrimpgram.models import Shrimp
from metergram.models import Meter
from django.db.models import Q
import weasyprint
import requests

@csrf_exempt
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
            #------- for App ---------
            url = "http://www.smarteolife.com/push/register.php"
            data_dict = {
                "CMD": "ACCOUNT_REG",
                "TOKEN_TYP": "uclone",
                "TOKEN_SER": "uclone",
                "TOKEN_PSW": request.POST['password'],
                "TOKEN_USR": request.POST['username'],
                "TOKEN_TEL": request.POST['last_name'],
                "TOKEN_EML": request.POST['email'],
                "TOKEN_TLK": " ",
            }
            requests.get(url, params=data_dict)
            #-------------------------
            return render(request, 'accounts/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':user_form})

class RegisterBtnView(CreateView):
    model = Meter
    fields = '__all__'
    #form_class = CloseForm
    template_name = 'accounts/register_btn.html'

@login_required
def account_list(request):
    group_name = request.user.groups.values_list('name', flat=True).first()
    files = User.objects.filter(groups__name=group_name)
    return render(request, 'accounts/account_list.html', {'files':files})

@login_required
def account_read(request):
    files = User.objects.filter(username=request.user.username)
    return render(request, 'accounts/account_read.html', {'files':files})

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('accounts:account_read')
    template_name = 'accounts/account_update.html'
    def authentication(self, request, pk):
        field_author = 'author'
        field_password = 'password'
        obj = User.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        password_field = getattr(obj, field_password)
        form = User(request.POST)
        form.instance.author = author_field
        form.instance.password = password_field

        if form.is_valid():
            form.save()
            # ------- for App ---------
            url = "http://www.smarteolife.com/push/register.php"
            data_dict = {
                "CMD": "ACCOUNT_REG",
                "TOKEN_TYP": "uclone",                          #request.POST['first_name'],
                "TOKEN_SER": "uclone",                          #request.POST['first_name'],
                "TOKEN_PSW": request.POST['password'],
                "TOKEN_USR": request.POST['username'],
                "TOKEN_TEL": request.POST['last_name'],
                "TOKEN_EML": request.POST['email'],
                "TOKEN_TLK": " ",
            }
            requests.get(url, params=data_dict)                 #response = requests.get(url, params=data_dict)
            # -----------------------
            return redirect('accounts:account_read')
        return render(request, 'accounts/account_update.html', {'form': form})

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:account_read')
    template_name = 'accounts/account_delete.html'
    def authentication(self, request, pk):
        #field_password = 'password'
        #obj = User.objects.filter(id=pk).first()
        #password_field = getattr(obj, field_password)
        # ------- for App ---------
        url = "http://www.smarteolife.com/push/register.php"
        data_dict = {
            "CMD": "ACCOUNT_DEL",
            "TOKEN_TYP": "uclone",                  #can use "del"      request.POST['first_name'],
            "TOKEN_SER": "uclone",                  #can use "del"      request.POST['first_name'],
            "TOKEN_PSW": request.user.password,
            "TOKEN_USR": request.user.username,
            "TOKEN_TEL": request.user.last_name,
            "TOKEN_EML": request.user.email,
            "TOKEN_TLK": " ",
        }
        requests.get(url, params=data_dict)             #response = requests.get(url, params=data_dict)  #print(response.status_code)
        # -----------------------
        return render(request, 'accounts/account_delete.html')

#for weasyprint
def generate_pdf(request):
    group_name = request.user.groups.values_list('name', flat=True).first()
    files = User.objects.filter(groups__name=group_name)
    html_string = render_to_string('accounts/pdf_list.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=account_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response




