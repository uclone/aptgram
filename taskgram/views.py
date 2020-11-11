from django.shortcuts import render, redirect
from .models import Task, Stask
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm, TaskForm
from django.db.models import Q

@login_required
def task_list(request):
    group_id = request.user.groups.values_list('id', flat=True).first()                    #for group_name, replace 'id' with 'name'
    pagefiles = Task.objects.filter(Q(author_id=request.user.id) & Q(group_id=group_id))
    #pagefiles = Task.objects.filter(author_id=request.user.id)
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
    return render(request, 'taskgram/task_list.html', {'files':files})

@login_required
def task_list_mobile(request):
    group_id = request.user.groups.values_list('id', flat=True).first()  # for group_name, replace 'id' with 'name'
    pagefiles = Task.objects.filter(Q(author_id=request.user.id) & Q(group_id=group_id))
    #pagefiles = Task.objects.filter(author_id=request.user.id)
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
    return render(request, 'taskgram/task_list_mobile.html', {'files':files})

@login_required
def task_search(request):
    group_id = request.user.groups.values_list('id', flat=True).first()                    #for group_name, replace 'id' with 'name'
    file_list = Task.objects.filter(Q(author_id=request.user.id) & Q(group_id=group_id))
    #file_list = Task.objects.filter(author_id=request.user.id)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs

    group_name = request.user.groups.values_list('name', flat=True).first()
    Stask.objects.filter(Q(author=request.user.username) & Q(group=group_name)).delete()
    #Stask.objects.filter(author=request.user.username).delete()

    for a in x:
        b = Stask(id=a.id, author=a.author.username, group=a.group.name, department=a.department, charge=a.charge,
                  subject=a.subject, task=a.task, photo=a.photo, manager=a.manager, director=a.director, response=a.response)
        b.save()
    return render(request, 'taskgram/task_search.html', {'filter': file_filter})

@login_required
def task_upload_mobile(request):
    form = TaskForm(request.POST, request.FILES)
    form.instance.author_id = request.user.id
    form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
    if form.is_valid():
        form.save()
        return redirect('taskgram:task_list_mobile')
    return render(request, 'taskgram/task_upload_mobile.html', {'form': form})

@login_required
def task_detail_mobile(request, pk):
    form = Task.objects.filter(id=pk)                                   # Model data
    return render(request, 'taskgram/task_detail_mobile.html', {'form': form})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('taskgram:task_list')
    template_name = 'taskgram/task_delete.html'

class TaskUploadView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = DateForm
    template_name = 'taskgram/task_upload.html'

    def post(self, request):
        instance = Task()
        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()

        if form.is_valid():
            form.save()
            return redirect('taskgram:task_list')
        return self.render_to_response({'form': form})

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = DateForm
    #fields = ['department', 'charge', 'subject', 'task', 'photo', 'manager', 'director', 'response']
    template_name = 'taskgram/task_update.html'

    def task_update(self, request, pk):
        instance = Task()
        obj = Task.objects.filter(id=pk).first()
        author_field = getattr(obj, 'author')
        photo_field = getattr(obj, 'photo')
        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author = author_field
        form.instance.photo = photo_field

        if form.is_valid():
            form.save()
            return redirect('taskgram:task_list')
        return render(request, 'taskgram/task_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    group_id = request.user.groups.values_list('id', flat=True).first()                    #for group_name, replace 'id' with 'name'
    files = Task.objects.filter(Q(author_id=request.user.id) & Q(group_id=group_id))
    html_string = render_to_string('taskgram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=task_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = Task.objects.filter(id=pk)                                   # Model data
    html_string = render_to_string('taskgram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=task_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    group_name = request.user.groups.values_list('name', flat=True).first()
    file_filter = Stask.objects.filter(Q(author=request.user.username) & Q(group=group_name))
    html_string = render_to_string('taskgram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=task_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
