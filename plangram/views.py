from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Plan, Splan, Schedule
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm
from sulbigram.models import Sulbi
from susungram.models import Susun
from django.utils import timezone


@login_required
def plan_list(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Plan.objects.filter(group_id=group_id)
    except:
        pagefiles = Plan.objects.filter(group_id=1)
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
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        file_list = Plan.objects.filter(group_id=group_id)
    except:
        file_list = Plan.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Splan.objects.all().delete()
    for a in x:
        b = Splan(id=a.id, start=a.start, close=a.close, department=a.department, charge=a.charge, subject=a.subject,
                  task=a.task, photo=a.photo, manager=a.manager, director=a.director, remark=a.remark)
        b.save()
    return render(request, 'plangram/plan_search.html', {'filter': file_filter})

def check_schedule(request):
    Schedule.objects.all().delete()
    group_id = request.user.groups.values_list('id', flat=True).first()
    sulbi_list = Sulbi.objects.filter(group_id=group_id)

    for a in sulbi_list:
        if a.start < timezone.now and a.close > timezone.now:
            b = Schedule(start=a.start, close=a.close, department=a.department, subject=a.subject, remark=a.remark)
            #b.pk = None                             #b.id = None
            b.save()

    susun_list = Susun.objects.filter(group_id=group_id)
    for a in susun_list:
        if a.start < timezone.now and a.close > timezone.now:
            b = Schedule(start=a.rule, close=a.plan, department=a.category, subject=a.subject, remark=a.treatment)
            #b.pk = None                             #b.id = None
            b.save()

    schedule_list = Schedule.objects.all()
    return render(request, 'plangram/schedule.html', {'files': schedule_list})

class PlanDeleteView(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = reverse_lazy('plangram:plan_list')
    template_name = 'plangram/plan_delete.html'

class PlanUploadView(LoginRequiredMixin, CreateView):
    model = Plan
    form_class = DateForm
    template_name = 'plangram/plan_upload.html'

    def post(self, request):
        form = DateForm(request.POST, request.FILES)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()
            return redirect('plangram:plan_list')
        return self.render_to_response({'form': form})

class PlanUpdateView(LoginRequiredMixin, UpdateView):
    model = Plan
    form_class = DateForm
    #fields = ['start', 'close', 'department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'remark']
    template_name = 'plangram/plan_update.html'

    def plan_update(self, request, pk):
        field_author = 'author'
        field_photo = 'photo'
        obj = Plan.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        photo_field = getattr(obj, field_photo)

        form = DateForm(request.POST, request.FILES)
        form.instance.author = author_field
        form.instance.photo = photo_field
        if form.is_valid():
            form.save()
            Plan.objects.filter(id=pk).delete()
            return redirect('plangram:plan_list')
        return render(request, 'plangram/plan_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        files = Plan.objects.filter(group_id=group_id)                             #.order_by('author')
    except:
        files = Plan.objects.filter(group_id=1)                                    #.order_by('author')

    html_string = render_to_string('plangram/pdf_list.html', {'files': files})              # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=plan_list_{}.pdf'.format(request.user)
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

def search_pdf(request):
    file_filter = Splan.objects.all()
    html_string = render_to_string('plangram/pdf_search.html', {'filter': file_filter})       # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=plan_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
