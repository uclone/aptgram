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

@login_required
def task_list(request):
    #try:
    #    request_user = request.user
    #    data = Task.objects.filter(author_id=request_user.id).first()
    #    pagefiles = Task.objects.filter(group_id=data.group_id)
    #except:
    #    pagefiles = Task.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name:
            pagefiles = Task.objects.filter(group_id=group_id)
        elif '2급' in request.user.last_name:
            pagefiles_1 = Task.objects.filter(group_id=group_id)
            pagefiles = pagefiles_1.objects.filter(department__icontains=user_dept)
        else:
            pagefiles = Task.objects.filter(author_id=request.user.id)
    except:
        pagefiles = Task.objects.filter(group_id=1)

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
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name:
            pagefiles = Task.objects.filter(group_id=group_id)
        elif '2급' in request.user.last_name:
            pagefiles_1 = Task.objects.filter(group_id=group_id)
            pagefiles = pagefiles_1.objects.filter(department__icontains=user_dept)
        else:
            pagefiles = Task.objects.filter(author_id=request.user.id)
    except:
        pagefiles = Task.objects.filter(author_id=1)

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
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name:
            file_list = Task.objects.filter(group_id=group_id)
        elif '2급' in request.user.last_name:
            file_list_1 = Task.objects.filter(group_id=group_id)
            file_list = file_list_1.objects.filter(department__icontains=user_dept)
        else:
            file_list = Task.objects.filter(author_id=request.user.id)
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
            user_dept = request.user.last_name[0:2]  # check User grade
            user_name = request.user.first_name
            if '1급' in request.user.last_name:                                       #or user_dept in instance.department:
                form.save()
            elif '2급' in request.user.last_name and user_name in instance.charge:
                form.instance.remark = ' '
                form.save()
            elif '3급' in request.user.last_name and user_name in instance.charge:
                form.instance.remark = ' '
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
        field_author = 'author'
        field_photo = 'photo'
        obj = Task.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        photo_field = getattr(obj, field_photo)

        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author = author_field
        form.instance.photo = photo_field
        if form.is_valid():
            user_dept = request.user.last_name[0:2]  # check User grade
            user_name = request.user.first_name
            if '1급' in request.user.last_name:                                       #or user_dept in instance.department:
                form.save()
            elif '2급' in request.user.last_name and user_dept in instance.department:
                form.save()
            elif '3급' in request.user.last_name and user_name in instance.charge:
                form.instance.remark = ' '
                form.save()
            Task.objects.filter(id=pk).delete()
            return redirect('taskgram:task_list')
        return render(request, 'taskgram/task_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name:
            files = Task.objects.filter(group_id=group_id)
        elif '2급' in request.user.last_name:
            files_1 = Task.objects.filter(group_id=group_id)
            files = files_1.objects.filter(department__icontains=user_dept)
        else:
            files = Task.objects.filter(author_id=request.user.id)
    except:
        files = Task.objects.filter(group_id=1)                                    #.order_by('author')

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
    file_filter = Stask.objects.all()
    html_string = render_to_string('taskgram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=task_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
