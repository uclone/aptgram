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

@login_required
def jumin_list(request):
    #request_user = request.user
    #gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    #data = Jumin.objects.filter(author_id=request_user.id).first()
    #pagefiles = Jumin.objects.filter(group_id=data.group_id)


    pagefiles = Jumin.objects.all()



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
    return render(request, 'jumingram/jumin_list.html', {'files':files})

@login_required
def jumin_search(request):
    #request_user = request.user
    #gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    #data = Jumin.objects.filter(author_id=request_user.id).first()
    #file_list = Jumin.objects.filter(group_id=data.group_id)


    file_list = Jumin.objects.all()



    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Sjumin.objects.all().delete()
    for a in x:
        b = Sjumin(id=a.dong, ho=a.ho, represent=a.represent, family=a.family, phone=a.phone,
                   car=a.car, date=a.date, remark=a.remark, file=a.file)
        b.save()
    return render(request, 'jumingram/jumin_search.html', {'filter': file_filter})

class JuminDeleteView(LoginRequiredMixin, DeleteView):
    model = Jumin
    success_url = reverse_lazy('jumingram:jumin_list')
    template_name = 'jumingram/jumin_delete.html'

class JuminUploadView(LoginRequiredMixin, CreateView):
    model = Jumin
    fields = ['dong', 'ho', 'represent', 'family', 'phone', 'car', 'date', 'remark', 'file']
    template_name = 'jumingram/jumin_upload.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('jumingram:jumin_list')
        else:
            return self.render_to_response({'form':form})

class JuminUpdateView(LoginRequiredMixin, UpdateView):
    model = Jumin
    fields = ['dong', 'ho', 'represent', 'family', 'phone', 'car', 'date', 'remark', 'file']
    template_name = 'jumingram/jumin_update.html'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('jumingram:jumin_list')
        else:
            return self.render_to_response({'form': form})

#for weasyprint
def generate_pdf(request):
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    files = Jumin.objects.filter(group_id=gr_id).order_by('author')                                          # Model data
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
    # user = auth.get_user(request)
    gr_id = request.user.groups.values_list('id', flat=True).first()  # for "group_name" use 'name' instead of 'id'
    file_filter = Sjumin.objects.filter(group_id=gr_id).order_by('author')
    html_string = render_to_string('jumingram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=jumin_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
