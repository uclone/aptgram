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

@login_required
def life_list(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    pagefiles = Life.objects.filter(group_id=gr_id)
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
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_list = Life.objects.filter(group_id=gr_id)
    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Slife.objects.all().delete()
    for a in x:
        b = Slife(id=a.id, contact=a.contact, subject=a.subject, task_1=a.task_1, photo_1=a.photo_1, charge=a.charge,
                  department=a.department, task_2=a.task_2, photo_2=a.photo_2, response=a.response)
        b.save()
    return render(request, 'lifegram/life_search.html', {'filter': file_filter})

class LifeDeleteView(LoginRequiredMixin, DeleteView):
    model = Life
    success_url = reverse_lazy('lifegram:life_list')
    template_name = 'lifegram/life_delete.html'

class LifeUploadView(LoginRequiredMixin, CreateView):
    model = Life
    fields = ['contact', 'subject', 'task_1', 'photo_1', 'charge', 'department', 'task_2', 'photo_2', 'response']
    template_name = 'lifegram/life_upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('lifegram:life_list')
        else:
            return self.render_to_response({'form':form})

class LifeUpdateView(LoginRequiredMixin, UpdateView):
    model = Life
    fields = ['contact', 'subject', 'task_1', 'photo_1', 'charge', 'department', 'task_2', 'photo_2', 'response']
    template_name = 'lifegram/life_update.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('lifegram:life_list')
        else:
            return self.render_to_response({'form': form})

#for weasyprint
def generate_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files = Life.objects.filter(group_id=gr_id).order_by('author')                                    # Model data
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
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_filter = Slife.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('lifegram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=life_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
