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
from .forms import DateForm

@login_required
def life_list(request):
    #try:
    #    request_user = request.user
    #    data = Life.objects.filter(author_id=request_user.id).first()
    #    pagefiles = Life.objects.filter(group_id=data.group_id)
    #except:
    #    pagefiles = Life.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Life.objects.filter(group_id=group_id)
    except:
        pagefiles = Life.objects.filter(group_id=1)

    #pagination - start
    page = request.GET.get('page', 1)
    paginator = Paginator(pagefiles, 3)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    #pagination - end
    return render(request, 'lifegram/life_list.html', {'files':files})

@login_required
def life_search(request):
    #try:
    #    request_user = request.user
    #    data = Life.objects.filter(author_id=request_user.id).first()
    #    file_list = Life.objects.filter(group_id=data.group_id)
    #except:
    #    file_list = Life.objects.filter(group_id=1)

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

class LifeDeleteView(LoginRequiredMixin, DeleteView):
    model = Life
    success_url = reverse_lazy('lifegram:life_list')
    template_name = 'lifegram/life_delete.html'

class LifeUploadView(LoginRequiredMixin, CreateView):
    model = Life
    form_class = DateForm
    template_name = 'lifegram/life_upload.html'

    def post(self, request):
        form = DateForm(request.POST)
        form.instance.author_id = self.request.user.id
        form.instance.group_id = self.request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.instance.save()
            return redirect('lifegram:life_upload')
        return self.render_to_response({'form': form})

class LifeUpdateView(LoginRequiredMixin, UpdateView):
    model = Life
    form_class = DateForm
    template_name = 'lifegram/life_update.html'

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
