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
def life_list_mobile(request):
    try:
        request_user = request.user
        pagefiles = Life.objects.filter(author_id=request_user.id)
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
    return render(request, 'lifegram/life_list_mobile.html', {'files':files})

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
        b = Slife(id=a.id, contact=a.contact, subject=a.subject, task_1=a.task_1, photo_1=a.photo_1, charge=a.charge,
                  department=a.department, date=a.date, close=a.close, task_2=a.task_2, photo_2=a.photo_2)
        b.save()
    return render(request, 'lifegram/life_search.html', {'filter': file_filter})

@login_required
def life_upload_mobile(request):
    form = LifeForm(request.POST, request.FILES)
    form.instance.author_id = request.user.id
    form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
    if form.is_valid():
        form.instance.save()
        return redirect('lifegram:life_list_mobile')
    return render(request, 'lifegram/life_upload_mobile.html', {'form': form})

@login_required
def life_detail_mobile(request, kk):
    form = Life.objects.filter(id=kk)                                   # Model data
    return render(request, 'lifegram/life_detail_mobile.html', {'form': form})

class LifeDeleteView(LoginRequiredMixin, DeleteView):
    model = Life
    success_url = reverse_lazy('lifegram:life_list')
    template_name = 'lifegram/life_delete.html'

class LifeUploadView(LoginRequiredMixin, CreateView):
    model = Life
    form_class = DateForm
    template_name = 'lifegram/life_upload.html'

    def post(self, request):
        form = DateForm(request.POST, request.FILES)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()
            return redirect('lifegram:life_list')
        return self.render_to_response({'form': form})

class LifeUpdateView(LoginRequiredMixin, UpdateView):
    model = Life
    form_class = DateForm
    #fields = ['department', 'charge', 'date', 'close', 'task_2', 'photo_2', 'response']
    template_name = 'lifegram/life_update.html'

    def life_update(self, request, pk):
        field_author = 'author'
        field_photo_2 = 'photo_2'
        obj = Life.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        photo_2_field = getattr(obj, field_photo_2)

        form = DateForm(request.POST, request.FILES)
        form.instance.author = author_field
        form.instance.photo = photo_2_field
        if form.is_valid():
            form.save()
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

def detail_pdf(request, kk):
    files = Life.objects.filter(id=kk)                                   # Model data
    html_string = render_to_string('lifegram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=life_detail_{}_{}.pdf'.format(request.user, kk)
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
