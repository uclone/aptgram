from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Equip, Sequip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter

@login_required
def equip_list(request):
    # user = auth.get_user(request)
#    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
#    pagefiles = Equip.objects.filter(group_id=gr_id)



    pagefiles = Equip.objects.all()
# - pagination - start
    page = request.GET.get('page', 1)
    paginator = Paginator(pagefiles, 6)
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
# - pagination - end
    return render(request, 'equipgram/equip_list.html', {'files':files})

@login_required
def equip_search(request):
    #user = auth.get_user(request)
    #gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    #file_list = Equip.objects.filter(group_id=gr_id)

    file_list = Equip.objects.all()
    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    Sequip.objects.all().delete()
    for a in x:
        b = Sequip(id=a.id, subject=a.subject, location=a.location, department=a.department, manager_1=a.manager_1,
                   manager_2=a.manager_2, spec=a.spec, date=a.date, remark=a.remark, photo=a.photo)
        b.save()
    return render(request, 'equipgram/equip_search.html', {'filter': file_filter})

class EquipDeleteView(LoginRequiredMixin, DeleteView):
    model = Equip
    success_url = reverse_lazy('equipgram:equip_list')
    template_name = 'equipgram/equip_delete.html'

class EquipUploadView(LoginRequiredMixin, CreateView):
    model = Equip
    fields = ['subject', 'location', 'department', 'manager_1', 'manager_2', 'spec', 'date', 'remark', 'photo']
    template_name = 'equipgram/equip_upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('equipgram:equip_list')
        else:
            return self.render_to_response({'form':form})

class EquipUpdateView(LoginRequiredMixin, UpdateView):
    model = Equip
    fields = ['subject', 'location', 'department', 'manager_1', 'manager_2', 'spec', 'date', 'remark', 'photo']
    template_name = 'equipgram/equip_update.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('equipgram:equip_list')
        else:
            return self.render_to_response({'form':form})

#for weasyprint
def generate_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files = Equip.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('equipgram/pdf_list.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=equip_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, kk):
    files = Equip.objects.filter(id=kk)                                        # Model data
    html_string = render_to_string('equipgram/pdf_detail.html', {'files': files})           # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=equip_detail_{}_{}.pdf'.format(request.user, kk)    #user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files_filter = Sequip.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('equipgram/pdf_search.html', {'filter': files_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=equip_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

