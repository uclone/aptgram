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
from django.contrib.auth import get_user
#from django.contrib.auth.models import Group

@login_required
def file_list(request):
    #request_user = request.user
    grrr_id = request.user.groups.values_list('id').first()  # for "group_name" use 'name' instead of 'id'
    gr_id = grrr_id[0]
    pagefiles = File.objects.filter(group_id=gr_id)
    #pagefiles = File.objects.filter(author=request.user)
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
    return render(request, 'filegram/file_list.html', {'files':files})

@login_required
def file_search(request):
    #request_user = request.user
    #group = File.objects.filter(author_id=request_user).first()
    #gr_id = xuser.group_id   #values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    grrr_id = request.user.groups.values_list('id').first()  # for "group_name" use 'name' instead of 'id'
    gr_id = grrr_id[0]
    file_list = File.objects.filter(group_id=gr_id)
    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Sfile.objects.all().delete()
    for a in x:
        b = Sfile(id=a.id, department=a.department, charge=a.charge, manager=a.manager, director=a.director,
                  super=a.super, subject=a.subject, abstract=a.abstract, file=a.file, remark=a.remark)
        b.save()
    return render(request, 'filegram/file_search.html', {'filter': file_filter})

class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = File
    success_url = reverse_lazy('filegram:file_list')
    template_name = 'filegram/file_delete.html'

class FileUploadView(LoginRequiredMixin, CreateView):
    model = File
    fields = ['department', 'charge', 'manager', 'director', 'super', 'subject', 'abstract', 'file', 'remark']
    template_name = 'filegram/file_upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('filegram:file_list')
        else:
            return self.render_to_response({'form':form})

class FileUpdateView(LoginRequiredMixin, UpdateView):
    model = File
    fields = ['department', 'charge', 'manager', 'director', 'super', 'subject', 'abstract', 'file', 'remark']
    template_name = 'filegram/file_update.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('filegram:file_list')
        else:
            return self.render_to_response({'form': form})

#for weasyprint
def generate_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files = File.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('filegram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=file_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, kk):
    files = File.objects.filter(id=kk)                                   # Model data
    html_string = render_to_string('filegram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=file_detail_{}_{}.pdf'.format(request.user, kk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_filter = Sfile.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('filegram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=file_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
