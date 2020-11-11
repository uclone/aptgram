from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import File, Sfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm

@login_required
def file_list(request):
    #try:
    #    request_user = request.user
    #    data = File.objects.filter(author_id=request_user.id).first()
    #    pagefiles = File.objects.filter(group_id=data.group_id)
    #except:
    #    pagefiles = File.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name:
            pagefiles = File.objects.filter(group_id=group_id)
        elif '2급' in request.user.last_name:
            pagefiles_1 = File.objects.filter(group_id=group_id)
            pagefiles = pagefiles_1.objects.filter(department__icontains=user_dept)
        else:
            pagefiles = File.objects.filter(author_id=request.user.id)
    except:
        pagefiles = File.objects.filter(group_id=1)

    #pagination - start
    page = request.GET.get('page', 1)
    paginator = Paginator(pagefiles, 10)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    #pagination - end
    return render(request, 'filegram/file_list.html', {'files':files})

@login_required
def file_search(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name:
            file_list = File.objects.filter(group_id=group_id)
        elif '2급' in request.user.last_name:
            file_list_1 = File.objects.filter(group_id=group_id)
            file_list = file_list_1.objects.filter(department__icontains=user_dept)
        else:
            file_list = File.objects.filter(author_id=request.user.id)
    except:
        file_list = File.objects.filter(group_id=1)

    #django-filter - start
    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Sfile.objects.filter(author=request.user.username).delete()
    for a in x:
        b = Sfile(id=a.id, author=a.author.username, group=a.group.name, department=a.department, charge=a.charge,
                  manager=a.manager, director=a.director, super=a.super, subject=a.subject, abstract=a.abstract)
        b.save()
    return render(request, 'filegram/file_search.html', {'filter': file_filter})

class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    success_url = reverse_lazy('filegram:file_list')
    template_name = 'filegram/file_delete.html'

class FileUploadView(LoginRequiredMixin, CreateView):
    model = File
    form_class = DateForm
    template_name = 'filegram/file_upload.html'

    def post(self, request):
        instance = File()
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
            return redirect('filegram:file_list')
        return self.render_to_response({'form': form})

def file_approval(request, pk):
    user_job = request.user.last_name
    instance = File()
    obj = File.objects.filter(id=pk).last()
    author_field = getattr(obj, 'author')
    group_field = getattr(obj, 'group')
    department_field = getattr(obj, 'department')
    subject_field = getattr(obj, 'subject')
    abstract_field = getattr(obj, 'abstract')
    file_field = getattr(obj, 'file')
    charge_field = getattr(obj, 'charge')
    manager_field = getattr(obj, 'manager')
    director_field = getattr(obj, 'director')
    board_field = getattr(obj, 'board')
    super_field = getattr(obj, 'super')
    visor_field = getattr(obj, 'visor')

    form = DateForm(request.POST, request.FILES, instance=instance)
    request.POST._mutable = True
    request.POST['department'] = department_field
    request.POST['subject'] = subject_field
    request.POST['abstract'] = abstract_field
    request.POST['file'] = file_field

    if '반장' not in user_job:
        request.POST['charge'] = charge_field
    if '과장' not in user_job:
        request.POST['manager'] = manager_field
    if '소장' not in user_job:
        request.POST['director'] = director_field
    if '이사' not in user_job:
        request.POST['board'] = board_field
    if '감사' not in user_job:
        request.POST['super'] = super_field
    if '회장' not in user_job:
        request.POST['visor'] = visor_field

    form.instance.author_id = request.user.id
    form.instance.group_id = request.user.groups.values_list('id', flat=True).last()
    form.instance.author = author_field
    form.instance.group = group_field

    if form.is_valid():
        user_dept = request.user.last_name[0:2]  # check User grade
        #user_name = request.user.first_name
        if '1급' in request.user.last_name:
            form.save()
        elif '2급' in request.user.last_name and user_dept in instance.department:
            form.save()
        elif '3급' in request.user.last_name and user_dept in instance.department:
            form.instance.remark = ' '
            form.save()
        return redirect('filegram:file_list')
    return render(request, 'filegram/file_approval.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name:
            files = File.objects.filter(group_id=group_id)
        elif '2급' in request.user.last_name:
            files_1 = File.objects.filter(group_id=group_id)
            files = files_1.objects.filter(department__icontains=user_dept)
        else:
            files = File.objects.filter(author_id=request.user.id)
    except:
        files = File.objects.filter(group_id=1)                                    #.order_by('author')

    html_string = render_to_string('filegram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=file_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = File.objects.filter(id=pk)                                   # Model data
    html_string = render_to_string('filegram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=file_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Sfile.objects.filter(author=request.user.username)
    html_string = render_to_string('filegram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=file_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

####################################################################################
#class FileUpdateView(LoginRequiredMixin, UpdateView):
#    model = File
#    form_class = DateForm
#    template_name = 'filegram/file_update.html'

#    def file_update(self, request, pk):
#        instance = File()
#        field_author = 'author'
#        field_file = 'file'
#        obj = File.objects.filter(id=pk).first()
#        author_field = getattr(obj, field_author)
#        file_field = getattr(obj, field_file)

#        form = DateForm(request.POST, request.FILES, instance=instance)
#        form.instance.author = author_field
#        form.instance.file = file_field
#        if form.is_valid():
#            user_dept = request.user.last_name[0:2]  # check User grade
#            user_name = request.user.first_name
#            if '1급' in request.user.last_name:                                       #or user_dept in instance.department:
#                form.save()
#            elif '2급' in request.user.last_name and user_dept in instance.department:
#                form.save()
#            elif '3급' in request.user.last_name and user_name in instance.charge:
#                form.instance.remark = ' '
#                form.save()
#            return redirect('filegram:file_list')
#        return render(request, 'filegram/file_update.html', {'form': form})