from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Sulbi, Ssulbi
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter

@login_required
def sulbi_list(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    pagefiles = Sulbi.objects.filter(group_id=gr_id)
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
    return render(request, 'sulbigram/sulbi_list.html', {'files':files})

@login_required
def sulbi_search(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_list = Sulbi.objects.filter(group_id=gr_id)
    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Ssulbi.objects.all().delete()
    for a in x:
        b = Ssulbi(id=a.id, department=a.department, subject=a.subject, action=a.action, start=a.start,
                   close=a.close, text=a.text, file=a.file, remark=a.remark)
        b.save()
    return render(request, 'sulbigram/sulbi_search.html', {'filter': file_filter})

class SulbiDeleteView(LoginRequiredMixin, DeleteView):
    model = Sulbi
    success_url = reverse_lazy('sulbigram:sulbi_list')
    template_name = 'sulbigram/sulbi_delete.html'

class SulbiUploadView(LoginRequiredMixin, CreateView):
    model = Sulbi
    fields = ['department', 'subject', 'action', 'start', 'close', 'text', 'file', 'remark']
    template_name = 'sulbigram/sulbi_upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('sulbigram:sulbi_list')
        else:
            return self.render_to_response({'form':form})

class SulbiUpdateView(LoginRequiredMixin, UpdateView):
    model = Sulbi
    fields = ['department', 'subject', 'action', 'start', 'close', 'text', 'file', 'remark']
    template_name = 'sulbigram/sulbi_update.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('sulbigram:sulbi_list')
        else:
            return self.render_to_response({'form':form})

#for weasyprint
def generate_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files = Sulbi.objects.filter(group_id=gr_id).order_by('author')                                    # Model data
    html_string = render_to_string('sulbigram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=sulbi_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, kk):
    files = Sulbi.objects.filter(id=kk)                                   # Model data
    html_string = render_to_string('sulbigram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=sulbi_detail_{}_{}.pdf'.format(request.user, kk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_filter = Ssulbi.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('sulbigram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=sulbi_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
