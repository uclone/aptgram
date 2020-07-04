from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Paper, Spaper
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm

@login_required
def paper_list(request):
    #try:
    #    request_user = request.user
    #    data = Paper.objects.filter(author_id=request_user.id).first()
    #    pagefiles = Paper.objects.filter(group_id=data.group_id)
    #except:
    #    pagefiles = Paper.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Paper.objects.filter(group_id=group_id)
    except:
        pagefiles = Paper.objects.filter(group_id=1)

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
    return render(request, 'papergram/paper_list.html', {'files':files})

@login_required
def paper_search(request):
    #try:
    #    request_user = request.user
    #    data = Plan.objects.filter(author_id=request_user.id).first()
    #    file_list = Plan.objects.filter(group_id=data.group_id)
    #except:
    #    file_list = Plan.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        file_list = Paper.objects.filter(group_id=group_id)
    except:
        file_list = Paper.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Spaper.objects.all().delete()
    for a in x:
        b = Spaper(id=a.id, subject=a.subject, description=a.description,)
        b.save()
    return render(request, 'papergram/paper_search.html', {'filter': file_filter})

class PaperDeleteView(LoginRequiredMixin, DeleteView):
    model = Paper
    success_url = reverse_lazy('papergram:paper_list')
    template_name = 'papergram/paper_delete.html'

class PaperUploadView(LoginRequiredMixin, CreateView):
    model = Paper
    form_class = DateForm
    template_name = 'papergram/paper_upload.html'

    def post(self, request):
        form = DateForm(request.POST, request.FILES)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()
            return redirect('papergram:paper_list')
        return self.render_to_response({'form': form})

class PaperUpdateView(LoginRequiredMixin, UpdateView):
    model = Paper
    form_class = DateForm
    template_name = 'papergram/paper_update.html'

    def paper_update(self, request, pk):
        field_author = 'author'
        field_file = 'file'
        obj = Paper.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        file_field = getattr(obj, field_file)

        form = DateForm(request.POST, request.FILES)
        form.instance.author = author_field
        form.instance.file = file_field
        if form.is_valid():
            form.save()
            Paper.objects.filter(id=pk).delete()
            return redirect('papergram:paper_list')
        return render(request, 'papergram/paper_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        files = Paper.objects.filter(group_id=group_id)                             #.order_by('author')
    except:
        files = Paper.objects.filter(group_id=1)                                    #.order_by('author')

    html_string = render_to_string('papergram/pdf_list.html', {'files': files})              # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=paper_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, kk):
    files = Paper.objects.filter(id=kk)                                                      # Model data
    html_string = render_to_string('papergram/pdf_detail.html', {'files': files})            # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=paper_detail_{}_{}.pdf'.format(request.user, kk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Spaper.objects.all()
    html_string = render_to_string('papergram/pdf_search.html', {'filter': file_filter})       # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=paper_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
