from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Life, Slife
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm, LifeForm
from django.contrib.auth.models import User, Group

@login_required
def life_list(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Life.objects.filter(group_id=group_id)
    except:
        pagefiles = Life.objects.filter(group_id=1)

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
    return render(request, 'lifegram/life_list.html', {'files':files})

@login_required
def life_list_jumin(request):
    try:
        request_user = request.user
        pagefiles = Life.objects.filter(author_id=request_user.id).filter(open='공개')
    except:
        pagefiles = Life.objects.filter(author_id=1)

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
    return render(request, 'lifegram/life_list_jumin.html', {'files':files})

@login_required
def life_search(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        file_list = Life.objects.filter(group_id=group_id)
    except:
        file_list = Life.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Slife.objects.all().delete()
    for a in x:
        b = Slife(id=a.id, applicant=a.applicant, created=a.created, subject=a.subject, task_1=a.task_1, photo_1=a.photo_1,
                  charge=a.charge, department=a.department, date=a.date, close=a.close, task_2=a.task_2, photo_2=a.photo_2)
        b.save()
    return render(request, 'lifegram/life_search.html', {'filter': file_filter})

@login_required
def life_upload_jumin(request):
    form = LifeForm(request.POST, request.FILES)
    form.instance.author_id = request.user.id
    form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
    if form.is_valid():
        form.save()
        return redirect('lifegram:life_list_jumin')
    return render(request, 'lifegram/life_upload_jumin.html', {'form': form})

class LifeUpdateJuminView(LoginRequiredMixin, UpdateView):
    model = Life
    form_class = LifeForm
    #fields = ['department', 'charge', 'date', 'close', 'task_2', 'photo_2', 'response']
    template_name = 'lifegram/life_update_jumin.html'

    def life_update(self, request, pk):
        instance = Life()
        user_dept = request.user.last_name[0:2]
        field_author = 'author'
        field_photo_1 = 'photo_1'
        obj = Life.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        photo_1_field = getattr(obj, field_photo_1)
        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author = author_field
        form.instance.photo_1 = photo_1_field
        if form.is_valid():
            if '1급' in request.user.last_name:                                                      #check User grade
                form.save()                                                                         #check User grade
            elif '2급' in request.user.last_name:
                if '리' not in request.user.last_name:                     # check User grade
                    form.save()
                elif user_dept in instance.department:
                    form.instance.remark = ' '
                    form.save()                                                                         # check User grade
            elif '3급' in request.user.last_name and user_dept in instance.department:               # check User grade
                form.instance.remark = ' '
                form.save()                                                                         # check User grade
            Life.objects.filter(id=pk).delete()
            return redirect('lifegram:life_list')
        return render(request, 'lifegram/life_update.html', {'form': form})

@login_required
def life_detail_jumin(request, pk):
    form = Life.objects.filter(id=pk)                                   # Model data
    return render(request, 'lifegram/life_detail_jumin.html', {'form': form})

class LifeDeleteView(LoginRequiredMixin, DeleteView):
    model = Life
    success_url = reverse_lazy('lifegram:life_list')
    template_name = 'lifegram/life_delete.html'

class LifeUploadView(LoginRequiredMixin, CreateView):
    model = Life
    form_class = DateForm
    template_name = 'lifegram/life_upload.html'

    def post(self, request):
        instance = Life()
        user_dept = request.user.last_name[0:2]
        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            if '1급' in request.user.last_name:                                       #or user_dept in instance.department:
                form.save()
            elif '2급' in request.user.last_name and user_dept in instance.department:
                form.save()
            elif '3급' in request.user.last_name and user_dept in instance.department:
                form.save()                                                                       # check User grade
            return redirect('lifegram:life_list')
        return self.render_to_response({'form': form})

class LifeUpdateView(LoginRequiredMixin, UpdateView):
    model = Life
    form_class = DateForm
    #fields = ['department', 'charge', 'date', 'close', 'task_2', 'photo_2', 'response']
    template_name = 'lifegram/life_update.html'

    def life_update(self, request, pk):
        instance = Life()
        user_dept = request.user.last_name[0:2]
        field_author = 'author'
        field_photo_2 = 'photo_2'
        obj = Life.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        photo_2_field = getattr(obj, field_photo_2)
        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author = author_field
        form.instance.photo_2 = photo_2_field
        if form.is_valid():
            if '1급' in request.user.last_name:                                                      #check User grade
                form.save()                                                                         #check User grade
            elif '2급' in request.user.last_name:
                if '리' not in request.user.last_name:                     # check User grade
                    form.save()
                elif user_dept in instance.department:
                    form.instance.remark = ' '
                    form.save()                                                                         # check User grade
            elif '3급' in request.user.last_name and user_dept in instance.department:               # check User grade
                form.instance.remark = ' '
                form.save()                                                                         # check User grade
            Life.objects.filter(id=pk).delete()
            return redirect('lifegram:life_list')
        return render(request, 'lifegram/life_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        files = Life.objects.filter(group_id=group_id)                             #.order_by('author')
    except:
        files = Life.objects.filter(group_id=1)                                    #.order_by('author')

    html_string = render_to_string('lifegram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=life_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = Life.objects.filter(id=pk)                                   # Model data
    html_string = render_to_string('lifegram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=life_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Slife.objects.all()
    html_string = render_to_string('lifegram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=life_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
