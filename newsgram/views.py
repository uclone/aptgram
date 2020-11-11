from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import News, Snews
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm, NewsForm, PhotoForm

@login_required
def broadcasting(request):
    return redirect("https://papago.naver.com")

@login_required
def news_list(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = News.objects.filter(group_id=group_id)
    except:
        pagefiles = News.objects.filter(group_id=1)
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
    return render(request, 'newsgram/news_list.html', {'files':files})

@login_required
def news_search(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        file_list = News.objects.filter(group_id=group_id)
    except:
        file_list = News.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Snews.objects.filter(author=request.user.username).delete()
    for a in x:
        b = Snews(id=a.id, author=a.author.username, group=a.group.name, dong=a.dong, ho=a.ho, date=a.date,
                  subject=a.subject, created=a.created, updated=a.updated,)
        b.save()
    return render(request, 'newsgram/news_search.html', {'filter': file_filter})

@login_required
def news_list_jumin(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        user_dong = request.user.last_name
        user_ho = request.user.first_name
        user_filter_1 = News.objects.filter(group_id=group_id)
        user_filter_2 = user_filter_1.filter(dong=user_dong).filter(dong='전체')
        user_filter_3 = user_filter_2.filter(dong=user_ho).filter(ho='전체')
        pagefiles = user_filter_3.filter(remark='결재').filter(remark='승인')
    except:
        pagefiles = News.objects.filter(group_id=1)
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
    return render(request, 'newsgram/news_list_jumin.html', {'files':files})

@login_required
def news_detail_jumin(request, pk):
    form = News.objects.filter(id=pk)
    return render(request, 'newsgram/news_detail_jumin.html', {'form': form})

class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('newsgram:news_list')
    template_name = 'newsgram/news_delete.html'

class NewsUploadView(LoginRequiredMixin, CreateView):
    model = News
    form_class = DateForm
    template_name = 'newsgram/news_upload.html'

    def post(self, request):
        form = DateForm(request.POST)
        form.instance.author_id = self.request.user.id
        form.instance.group_id = self.request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            if '1급' not in request.user.last_name:
                form.instance.remark=' '
            form.save()
            return redirect('newsgram:news_list')
        return self.render_to_response({'form': form})

class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'newsgram/news_update.html'

    def news_update(self, request, pk):
        #instance = News()
        field_author = 'author'
        field_file = 'file'
        obj = News.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        file_field = getattr(obj, field_file)

        form = DateForm(request.POST)
        form.instance.author = author_field
        form.instance.file = file_field
        if form.is_valid():
            if '1급' not in request.user.last_name:
                form.instance.remark=' '
            form.save()
#            News.objects.filter(id=pk).delete()
            return redirect('newsgram:news_list')
        return render(request, 'newsgram/news_update.html', {'form': form})

class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    form_class = PhotoForm
    template_name = 'newsgram/news_update.html'

    def photo_update(self, request, pk):
        instance = News()
        field_author = 'author'
        field_photo = 'photo'
        obj = News.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        photo_field = getattr(obj, field_photo)

        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author = author_field
        form.instance.photo = photo_field
        if form.is_valid():
            if '1급' not in request.user.last_name:
                form.instance.remark=' '
            form.save()
#            News.objects.filter(id=pk).delete()
            return redirect('newsgram:news_list')
        return render(request, 'newsgram/news_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        files = News.objects.filter(group_id=group_id)                             #.order_by('author')
    except:
        files = News.objects.filter(group_id=1)                                    #.order_by('author')

    html_string = render_to_string('newsgram/pdf_list.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=news_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = News.objects.filter(id=pk)                                   # Model data
    html_string = render_to_string('newsgram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=news_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Snews.objects.filter(author=request.user.username)
    html_string = render_to_string('newsgram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=news_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
