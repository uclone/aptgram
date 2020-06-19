from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Meter, Smeter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import MeterForm

@login_required
def meter_list(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    pagefiles = Meter.objects.filter(group_id=gr_id)
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
    return render(request, 'metergram/meter_list.html', {'files':files})

@login_required
def meter_search(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_list = Meter.objects.filter(group_id=gr_id)
    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Smeter.objects.all().delete()
    for a in x:
        b = Smeter(id=a.id, dong=a.dong, ho=a.ho, utility=a.utility, serial=a.serial, mtr=a.mtr, cor=a.cor,
                   amount=a.amount, action=a.action, charge=a.charge, manager=a.manager)
        b.save()
    return render(request, 'metergram/meter_search.html', {'filter': file_filter})

def meter_post(request):
    if request.method == 'POST':
        form = MeterForm(request.POST)
        form.instance.author_id = request.user.id
        gr_id = request.user.groups.values_list('id', flat=True).first()
        form.instance.group_id = gr_id
        if form.is_valid():
            form.save()
            file = Meter.objects.order_by('-id')[:3]
            return render(request, 'metergram/meter_post.html', {'data': file})
    else:
        file = Meter.objects.order_by('-id')[:3]
    return render(request, 'metergram/meter_post.html', {'data': file})

class MeterDeleteView(LoginRequiredMixin, DeleteView):
    model = Meter
    success_url = reverse_lazy('metergram:meter_list')
    template_name = 'metergram/meter_delete.html'

class MeterUploadView(LoginRequiredMixin, CreateView):
    model = Meter
    fields = ['dong', 'ho', 'utility', 'serial', 'mtr', 'cor', 'amount', 'action', 'charge', 'manager']
    template_name = 'metergram/meter_upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('metergram:meter_list')
        else:
            return self.render_to_response({'form':form})

class MeterUpdateView(LoginRequiredMixin, UpdateView):
    model = Meter
    fields = ['dong', 'ho', 'utility', 'serial', 'mtr', 'cor', 'amount', 'action', 'charge', 'manager']
    template_name = 'metergram/meter_update.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('metergram:meter_list')
        else:
            return self.render_to_response({'form': form})

#for weasyprint
def generate_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files = Meter.objects.filter(group_id=gr_id).order_by('author')                                    # Model data
    html_string = render_to_string('metergram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=meter_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, kk):
    files = Meter.objects.filter(id=kk)                                   # Model data
    html_string = render_to_string('metergram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=meter_detail_{}_{}.pdf'.format(request.user, kk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_filter = Smeter.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('metergram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=meter_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response