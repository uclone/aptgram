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
from .filters import SearchFilter
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

def jumin_list_date(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Jumin.objects.filter(group_id=group_id).order_by('-date')
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
    return render(request, 'jumingram/jumin_list_date.html', {'files':files})

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
        b = Sjumin(id=a.id, dong=a.dong, ho=a.ho, represent=a.represent, family=a.family, phone=a.phone,
                   car=a.car, date=a.date, remark=a.remark)
        b.save()
    return render(request, 'jumingram/jumin_search.html', {'filter': file_filter})

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

    html_string = render_to_string('jumingram/pdf_list.html', {'files': files})                 # Rendered
    response = HttpResponse(content_type='application/pdf;')                                    # Creating http response
    response['Content-Disposition'] = 'filename=jumin_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response, stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = Jumin.objects.filter(id=pk)                                                         # Model data
    html_string = render_to_string('jumingram/pdf_detail.html', {'files': files})               # Rendered
    response = HttpResponse(content_type='application/pdf;')                                    # Creating http response
    response['Content-Disposition'] = 'filename=jumin_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response, stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Sjumin.objects.all()
    html_string = render_to_string('jumingram/pdf_search.html', {'filter': file_filter})        # Rendered
    response = HttpResponse(content_type='application/pdf;')                                    # Creating http response
    response['Content-Disposition'] = 'filename=jumin_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response, stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response


