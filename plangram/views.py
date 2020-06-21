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

@login_required
def plan_list(request):
    request_user = request.user
    #gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    data = Plan.objects.filter(author_id=request_user.id).first()
    pagefiles = Plan.objects.filter(group_id=data.group_id)

    # pagination - start
    page = request.GET.get('page', 1)
    paginator = Paginator(pagefiles, 3)
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
    request_user = request.user
    #gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    data = Plan.objects.filter(author_id=request_user.id).first()
    file_list = Plan.objects.filter(group_id=data.group_id)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Splan.objects.all().delete()
    for a in x:
        b = Splan(id=a.id, start=a.start, close=a.close, department=a.department, subject=a.subject,
                  task=a.task, photo=a.photo, manager=a.manager, director=a.director, remark=a.remark)
        b.save()
    return render(request, 'plangram/plan_search.html', {'filter': file_filter})

class PlanDeleteView(LoginRequiredMixin, DeleteView):
    model = Plan
    success_url = reverse_lazy('plangram:plan_list')
    template_name = 'plangram/plan_delete.html'

class PlanUploadView(LoginRequiredMixin, CreateView):
    model = Plan
    fields = ['start', 'close', 'department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'remark']
    template_name = 'plangram/plan_upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('plangram:plan_list')
        else:
            return self.render_to_response({'form':form})

class PlanUpdateView(LoginRequiredMixin, UpdateView):
    model = Plan
    fields = ['start', 'close', 'department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'remark']
    template_name = 'plangram/plan_update.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('plangram:plan_list')
        else:
            return self.render_to_response({'form':form})


#for weasyprint
def generate_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files = Plan.objects.filter(group_id=gr_id).order_by('author')                                           # Model data
    html_string = render_to_string('plangram/pdf_list.html', {'files': files})              # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=plan_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, kk):
    files = Plan.objects.filter(id=kk)                                                      # Model data
    html_string = render_to_string('plangram/pdf_detail.html', {'files': files})            # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=plan_detail_{}_{}.pdf'.format(request.user, kk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_filter = Splan.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('plangram/pdf_search.html', {'filter': file_filter})       # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=plan_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
