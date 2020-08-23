from django.shortcuts import render, redirect
from .forms import RegisterForm, UpdateForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
import weasyprint


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
            return render(request, 'accounts/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':user_form})

@login_required
def account_list(request):
    group_name = request.user.groups.values_list('name', flat=True).first()
    files = User.objects.filter(groups__name=group_name)
    return render(request, 'accounts/account_list.html', {'files':files})

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UpdateForm
    #fields = {'username', 'last_name', 'first_name'}
    success_url = reverse_lazy('accounts:account_list')
    template_name = 'accounts/account_update.html'

    def authentication(self, request, pk):
        field_author = 'author'
        obj = User.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)

        form = User(request.POST)
        form.instance.author = author_field
        if form.is_valid():
            form.save()
            User.objects.filter(id=pk).delete()
            return redirect('accounts:account_list')
        return render(request, 'accounts/account_update.html', {'form': form})

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:account_list')
    template_name = 'accounts/account_delete.html'

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


