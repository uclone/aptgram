from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Plan, Splan
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm, IssueForm
from django.utils import timezone
from datetime import datetime, timedelta, date


@login_required
def plan_list(request):
    pagefiles = Plan.objects.filter(author_id=request.user.id)
    # pagination - start
    page = request.GET.get('page', 1)
    paginator = Paginator(pagefiles, 10)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    # pagination - end
    return render(request, 'plangram/plan_list.html', {'files':files})

@login_required
def plan_search(request):
    file_list = Plan.objects.filter(author_id=request.user.id)
    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Splan.objects.all().delete()
    for a in x:
        b = Splan(id=a.id, department=a.department, subject=a.subject, created=a.created, updated=a.updated)
        b.save()
    return render(request, 'plangram/plan_search.html', {'filter': file_filter})

class PlanDeleteView(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = reverse_lazy('plangram:plan_list')
    template_name = 'plangram/plan_delete.html'

class PlanUploadView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = DateForm
    template_name = 'plangram/plan_upload.html'

    def post(self, request):
        instance = Plan()
        form = DateForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.instance.regpsw = form.instance.regpsw.zfill(6)
            form.save()
            return redirect('plangram:plan_list')
        return self.render_to_response({'form': form})

@login_required
def plan_password(request):
    pagefiles = Plan.objects.filter(author_id=request.user.id).first()
    return render(request, 'plangram/plan_password.html', {'files':pagefiles})

def plan_issue(request, pk):
    instance = Plan()
    obj = Plan.objects.filter(id=pk).first()
    author_field = getattr(obj, 'author')
    group_field = getattr(obj, 'group')
    regpsw_field = getattr(obj, 'regpsw')
    department_field = getattr(obj, 'department')
    subject_field = getattr(obj, 'subject')

    form = IssueForm(request.POST, instance=instance)
    request.POST._mutable = True
    request.POST['author'] = author_field
    request.POST['regpsw'] = regpsw_field

    form.instance.author_id = request.user.id
    form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
    form.instance.author = author_field
    form.instance.group = group_field
    form.instance.regpsw = regpsw_field
    form.instance.department = department_field
    form.instance.subject = subject_field

    if request.POST and form.is_valid():
        psw = ''
        reg = form.instance.regpsw.zfill(6)
        user = form.instance.author.username.zfill(6)
        for k in range(0, 6):
            psw += calc_psw_digit(reg, user, k, k + 1)
        form.instance.usepsw = psw
        form.save()
        return redirect('plangram:plan_password')
    return render(request, 'plangram/plan_issue.html', {'form': form})

def calc_psw_digit(reg, user, s, e):
    a = ord(reg[s:e])
    ax = ord(user[0:1]) + ord(user[1:2])
    a += ax
    micro = int(datetime.now().microsecond)
    micro3 = round(micro / 100)
    micro4 = round(micro / 1000)
    if s % 6 == 0:
        b = int(datetime.now().hour)
        b += micro4
    if s % 6 == 1:
        b = int(datetime.now().second)
        b += micro3
    if s % 6 == 2:
        b = int(datetime.now().minute)
        b += micro3
    if s % 6 == 3:
        b = int(datetime.now().hour)
        b += micro4
    if s % 6 == 4:
        b = int(datetime.now().minute)
        b += micro4
    if s % 6 == 5:
        b = int(datetime.now().microsecond)
        b += micro3

    a += b
    a %= 36
    a += 48
    if a > 57:
        a += 7
    return chr(a)

def generate_pdf(request):
    #try:
    #    group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
    #    files = Plan.objects.filter(group_id=group_id)                             #.order_by('author')
    #except:
    #    files = Plan.objects.filter(group_id=1)                                    #.order_by('author')
    files = Plan.objects.filter(author_id=request.user.id)
    html_string = render_to_string('plangram/pdf_list.html', {'files': files})              # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=plan_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Splan.objects.all()
    html_string = render_to_string('plangram/pdf_search.html', {'filter': file_filter})       # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=plan_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = Plan.objects.filter(id=pk)                                                      # Model data
    html_string = render_to_string('plangram/pdf_detail.html', {'files': files})            # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=plan_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
