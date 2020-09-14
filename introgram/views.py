from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Intro, Sintro
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm, IntroForm, PhotoForm

@login_required
def intro_list(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Intro.objects.filter(group_id=group_id)
    except:
        pagefiles = Intro.objects.filter(group_id=1)
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
    return render(request, 'introgram/intro_list.html', {'files':files})

@login_required
def intro_search(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        file_list = Intro.objects.filter(group_id=group_id)
    except:
        file_list = Intro.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Sintro.objects.all().delete()
    for a in x:
        b = Sintro(id=a.id, dong=a.dong, ho=a.ho, date=a.date, subject=a.subject, created=a.created, updated=a.updated,)
        b.save()
    return render(request, 'introgram/intro_search.html', {'filter': file_filter})

@login_required
def intro_list_jumin(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        user_dong = request.user.last_name
        user_ho = request.user.first_name
        user_filter_1 = Intro.objects.filter(group_id=group_id)
        user_filter_2 = user_filter_1.filter(dong=user_dong).filter(dong='전체')
        user_filter_3 = user_filter_2.filter(dong=user_ho).filter(ho='전체')
        pagefiles = user_filter_3.filter(remark='결재').filter(remark='승인')
    except:
        pagefiles = Intro.objects.filter(group_id=1)
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
    return render(request, 'introgram/intro_list_jumin.html', {'files':files})

@login_required
def intro_detail_jumin(request, pk):
    form = Intro.objects.filter(id=pk)
    return render(request, 'introgram/intro_detail_jumin.html', {'form': form})

class IntroDeleteView(LoginRequiredMixin, DeleteView):
    model = Intro
    success_url = reverse_lazy('introgram:intro_list')
    template_name = 'introgram/intro_delete.html'

class IntroUploadView(LoginRequiredMixin, CreateView):
    model = Intro
    form_class = DateForm
    template_name = 'introgram/intro_upload.html'

    def post(self, request):
        form = DateForm(request.POST)
        form.instance.author_id = self.request.user.id
        form.instance.group_id = self.request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            if '1급' not in request.user.last_name:
                form.instance.remark=' '
            form.save()
            return redirect('introgram:intro_list')
        return self.render_to_response({'form': form})

class IntroUpdateView(LoginRequiredMixin, UpdateView):
    model = Intro
    form_class = IntroForm
    template_name = 'introgram/intro_update.html'

    def intro_update(self, request, pk):
        field_author = 'author'
        field_file = 'file'
        obj = Intro.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        file_field = getattr(obj, field_file)

        form = IntroForm(request.POST)
        form.instance.author = author_field
        form.instance.file = file_field
        if form.is_valid():
            if '1급' not in request.user.last_name:
                form.instance.remark=' '
            form.save()
            Intro.objects.filter(id=pk).delete()
            return redirect('introgram:intro_list')
        return render(request, 'introgram/intro_update.html', {'form': form})

class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Intro
    form_class = PhotoForm
    template_name = 'introgram/intro_update.html'

    def photo_update(self, request, pk):
        field_author = 'author'
        field_photo = 'photo'
        obj = Intro.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        photo_field = getattr(obj, field_photo)

        form = PhotoForm(request.POST)
        form.instance.author = author_field
        form.instance.photo = photo_field
        if form.is_valid():
            if '1급' not in request.user.last_name:
                form.instance.remark=' '
            form.save()
            Intro.objects.filter(id=pk).delete()
            return redirect('introgram:intro_list')
        return render(request, 'introgram/intro_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()                 #for group_name, replace 'id' with 'name'
        files = Intro.objects.filter(group_id=group_id)                                      #.order_by('author')
    except:
        files = Intro.objects.filter(group_id=1)                                             #.order_by('author')

    html_string = render_to_string('introgram/pdf_list.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=intro_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = Intro.objects.filter(id=pk)                                                      # Model data
    html_string = render_to_string('introgram/pdf_detail.html', {'files': files})           # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=intro_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Sintro.objects.all()
    html_string = render_to_string('introgram/pdf_search.html', {'filter': file_filter})    # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=intro_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response