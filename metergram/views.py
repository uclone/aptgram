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
from .forms import MeterForm, DateForm

@login_required
def meter_list(request):
    #try:
    #    request_user = request.user
    #    data = Meter.objects.filter(author_id=request_user.id).first()
    #    pagefiles = Meter.objects.filter(group_id=data.group_id)
    #except:
    #    pagefiles = Meter.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Meter.objects.filter(group_id=group_id)
    except:
        pagefiles = Meter.objects.filter(group_id=1)

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
    return render(request, 'metergram/meter_list.html', {'files':files})

@login_required
def meter_list_author(request):
    try:
        request_user = request.user
        pagefiles = Meter.objects.filter(author_id=request_user.id)
    except:
        pagefiles = Meter.objects.filter(author_id=1)

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
    return render(request, 'metergram/meter_list_author.html', {'files':files})

@login_required
def meter_search(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        file_list = Meter.objects.filter(group_id=group_id)
    except:
        file_list = Meter.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Smeter.objects.all().delete()
    for a in x:
        b = Smeter(id=a.id, dong=a.dong, ho=a.ho, mtr=a.mtr, cor=a.cor, elec=a.elec, water=a.water,
                   action=a.action, charge=a.charge, manager=a.manager)
        b.save()
    return render(request, 'metergram/meter_search.html', {'filter': file_filter})

#def meter_post(request):
#    if request.method == 'POST':
#        form = MeterForm(request.POST)
#        form.instance.author_id = request.user.id
#        gr_id = request.user.groups.values_list('id', flat=True).first()
#        form.instance.group_id = gr_id
#        if form.is_valid():
#            form.save()
#            file = Meter.objects.order_by('-id')[:3]
#            return render(request, 'metergram/meter_post.html', {'data': file})
#    else:
#        file = Meter.objects.order_by('-id')[:3]
#    return render(request, 'metergram/meter_post.html', {'data': file})

def meter_post(request):
    form = MeterForm(request.POST)
    form.instance.author_id = request.user.id
    form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
    if form.is_valid():
        form.instance.save()
        return redirect('metergram:meter_list')
    return render(request, 'metergram/meter_post.html', {'form': form})

class MeterDeleteView(LoginRequiredMixin, DeleteView):
    model = Meter
    success_url = reverse_lazy('metergram:meter_list')
    template_name = 'metergram/meter_delete.html'

class MeterUploadView(LoginRequiredMixin, CreateView):
    model = Meter
    form_class = DateForm
    template_name = 'metergram/meter_upload.html'

    def post(self, request):
        form = DateForm(request.POST)
        form.instance.author_id = self.request.user.id
        form.instance.group_id = self.request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.instance.save()
            return redirect('metergram:meter_upload')
        return self.render_to_response({'form': form})

class MeterUpdateView(LoginRequiredMixin, UpdateView):
    model = Meter
    form_class = DateForm
    template_name = 'metergram/meter_update.html'

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        files = Meter.objects.filter(group_id=group_id)                             #.order_by('author')
    except:
        files = Meter.objects.filter(group_id=1)                                    #.order_by('author')

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
    file_filter = Smeter.objects.all()
    html_string = render_to_string('metergram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=meter_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response