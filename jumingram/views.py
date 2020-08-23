from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Jumin, Sjumin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter, GongoFilter
from .forms import DateForm

@login_required
def jumin_list(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Jumin.objects.filter(group_id=group_id)
    except:
        pagefiles = Jumin.objects.filter(group_id=1)
    # pagination - start --------------
    page = request.GET.get('page', 1)
    paginator = Paginator(pagefiles, 10)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    # pagination - end ----------------
    return render(request, 'jumingram/jumin_list.html', {'files':files})

@login_required
def jumin_search(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        file_list = Jumin.objects.filter(group_id=group_id)
    except:
        file_list = Jumin.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Sjumin.objects.all().delete()

    for a in x:
        b = Sjumin(id=a.dong, ho=a.ho, represent=a.represent, family=a.family, phone=a.phone,
                   car=a.car, date=a.date, remark=a.remark)
        b.save()
    return render(request, 'jumingram/jumin_search.html', {'filter': file_filter})

class GongoUpdateView(LoginRequiredMixin, UpdateView):
    model = Jumin
    fields = [ 'dong', 'ho', 'photo', 'file', 'task_apt', 'task_dong', 'task_ho']
    template_name = 'jumingram/gongo_update.html'

    def jumin_update(self, request, pk):
        field_author = 'author'
        field_photo = 'photo'
        field_file = 'file'
        obj = Jumin.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        photo_field = getattr(obj, field_photo)
        file_field = getattr(obj, field_file)

        form = Jumin(request.POST)
        form.instance.author = author_field
        form.instance.photo = photo_field
        form.instance.file = file_field
        if form.is_valid():
            form.save()
            #Jumin.objects.filter(id=pk).delete()
            return redirect('jumingram:jumin_list')
        return render(request, 'jumingram/gongo_update.html', {'form': form})

@login_required
def gongo_cast(request):
    obj = Jumin.objects.filter(author_id=request.user.id).last()
    dong_field = getattr(obj, 'dong')
    ho_field = getattr(obj, 'ho')
    photo_field = getattr(obj, 'photo')
    file_field = getattr(obj, 'file')
    task_apt_field = getattr(obj, 'task_apt')
    task_dong_field = getattr(obj, 'task_dong')
    task_ho_field = getattr(obj, 'task_ho')

    group_id = request.user.groups.values_list('id', flat=True).first()
    gongo_all = Jumin.objects.filter(group_id=group_id)
    gongo_dong = gongo_all.filter(dong=dong_field)
    gongo_ho = gongo_dong.filter(ho=ho_field)
    gongo = gongo_all
    if dong_field != '전체':
        gongo = gongo_dong
        if ho_field != '전체':
            gongo = gongo_ho

    for a in gongo:
        a.photo = photo_field
        a.file = file_field
        a.task_apt = task_apt_field
        a.task_dong = task_dong_field
        a.task_ho = task_ho_field
        a.save()

    else:
        return render(request, 'jumingram/gongo_cast.html', {'files': gongo})
    return render(request, 'jumingram/gongo_cast.html', {'files': gongo})

@login_required
def jumin_detail_mobile(request):
    group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
    file_list = Jumin.objects.filter(group_id=group_id)
    form_list = file_list.filter(dong=request.user.last_name)
    form = form_list.filter(ho=request.user.first_name)                         #.first()   # Model data
    return render(request, 'jumingram/jumin_detail_mobile.html', {'form': form})

class JuminDeleteView(LoginRequiredMixin, DeleteView):
    model = Jumin
    success_url = reverse_lazy('jumingram:jumin_list')
    template_name = 'jumingram/jumin_delete.html'

class JuminUploadView(LoginRequiredMixin, CreateView):
    model = Jumin
    form_class = DateForm
    template_name = 'jumingram/jumin_upload.html'

    def post(self, request):
        form = DateForm(request.POST)
        form.instance.author_id = self.request.user.id
        form.instance.group_id = self.request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()
            return redirect('jumingram:jumin_list')
        return self.render_to_response({'form': form})

class JuminUpdateView(LoginRequiredMixin, UpdateView):
    model = Jumin
    form_class = DateForm
    template_name = 'jumingram/jumin_update.html'

    def jumin_update(self, request, pk):
        field_author = 'author'
        obj = Jumin.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)

        form = DateForm(request.POST)
        form.instance.author = author_field
        if form.is_valid():
            form.save()
            Jumin.objects.filter(id=pk).delete()
            return redirect('jumingram:jumin_list')
        return render(request, 'jumingram/jumin_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        files = Jumin.objects.filter(group_id=group_id)                             #.order_by('author')
    except:
        files = Jumin.objects.filter(group_id=1)                                    #.order_by('author')

    html_string = render_to_string('jumingram/pdf_list.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=jumin_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, kk):
    files = Jumin.objects.filter(id=kk)                                   # Model data
    html_string = render_to_string('jumingram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=jumin_detail_{}_{}.pdf'.format(request.user, kk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Sjumin.objects.all()
    html_string = render_to_string('jumingram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=jumin_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
