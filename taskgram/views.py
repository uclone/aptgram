from django.shortcuts import render
from .models import Task, Stask
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter

@login_required
def task_list(request):
    #try:
    #    request_user = request.user
    #    data = Task.objects.filter(author_id=request_user.id).first()
    #    pagefiles = Task.objects.filter(group_id=data.group_id)
    #except:
    #    pagefiles = Task.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Task.objects.filter(group_id=group_id)
    except:
        pagefiles = Task.objects.filter(group_id=1)

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
    return render(request, 'taskgram/task_list.html', {'files':files})

@login_required
def task_search(request):
    #try:
    #    request_user = request.user
    #    data = Task.objects.filter(author_id=request_user.id).first()
    #    file_list = Task.objects.filter(group_id=data.group_id)
    #except:
    #    file_list = Task.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        file_list= Task.objects.filter(group_id=group_id)
    except:
        file_list = Task.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Stask.objects.all().delete()
    for a in x:
        b = Stask(id=a.id, department=a.department, charge=a.charge, subject=a.subject, task=a.task,
                  photo=a.photo, manager=a.manager, director=a.director, response=a.response)
        b.save()
    return render(request, 'taskgram/task_search.html', {'filter': file_filter})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('taskgram:task_list')
    template_name = 'taskgram/task_delete.html'

class TaskUploadView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'response']
    template_name = 'taskgram/task_upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        form.instance.group_id = self.request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.instance.save()
            return redirect('taskgram:task_list')
        else:
            return self.render_to_response({'form':form})

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'response']
    template_name = 'taskgram/task_update.html'

    def form_valid(self, form):
        form.instance.author_id == self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('taskgram:task_list')
        else:
            return self.render_to_response({'form': form})

#for weasyprint
def generate_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files = Task.objects.filter(group_id=gr_id).order_by('author')                                    # Model data
    html_string = render_to_string('taskgram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=task_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, kk):
    files = Task.objects.filter(id=kk)                                   # Model data
    html_string = render_to_string('taskgram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=task_detail_{}_{}.pdf'.format(request.user, kk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_filter = Stask.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('taskgram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=task_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
