from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Sulbi, Ssulbi
from timegram.models import Time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm
from django.db.models import Q

@login_required
def sulbi_list(request):
    #try:
    #    group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
    #    user_dept = request.user.last_name[0:2]                                     #for user's department
    #    if '1급' in request.user.last_name or '2급' in request.user.last_name:
    #        pagefiles = Sulbi.objects.filter(group_id=group_id)
    #    else:
    #        pagefiles_1 = Sulbi.objects.filter(group_id=group_id)
    #        pagefiles = pagefiles_1.objects.filter(department__icontains=user_dept)
    #except:
    #    pagefiles = Sulbi.objects.filter(group_id=1)

    group_id = request.user.groups.values_list('id', flat=True).first()                    #for group_name, replace 'id' with 'name'
    pagefiles = Sulbi.objects.filter(Q(author_id=request.user.id) & Q(group_id=group_id))
    #pagefiles = Sulbi.objects.filter(author_id=request.user.id)

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
    return render(request, 'sulbigram/sulbi_list.html', {'files':files})

@login_required
def sulbi_search(request):
    #try:
    #    request_user = request.user
    #    data = Sulbi.objects.filter(author_id=request_user.id).first()
    #    file_list = Sulbi.objects.filter(group_id=data.group_id)
    #except:
    #    file_list = Sulbi.objects.filter(group_id=1)

    group_id = request.user.groups.values_list('id', flat=True).first()                    #for group_name, replace 'id' with 'name'
    file_list = Sulbi.objects.filter(Q(author_id=request.user.id) & Q(group_id=group_id))
    #file_list = Sulbi.objects.filter(author_id=request.user.id)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs

    group_name = request.user.groups.values_list('name', flat=True).first()
    Ssulbi.objects.filter(Q(author=request.user.username) & Q(group=group_name)).delete()
    #Ssulbi.objects.filter(author=request.user.username).delete()

    for a in x:
        b = Ssulbi(id=a.id, author=a.author.username, group=a.group.name, department=a.department, subject=a.subject,
                   action=a.action, start=a.start, close=a.close, text=a.text, file=a.file, remark=a.remark)
        b.save()
    return render(request, 'sulbigram/sulbi_search.html', {'filter': file_filter})

class SulbiDeleteView(LoginRequiredMixin, DeleteView):
    model = Sulbi
    success_url = reverse_lazy('sulbigram:sulbi_list')
    template_name = 'sulbigram/sulbi_delete.html'

class SulbiUploadView(LoginRequiredMixin, CreateView):
    model = Sulbi
    form_class = DateForm
    template_name = 'sulbigram/sulbi_upload.html'

    def post(self, request):
        instance = Sulbi()
        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()                                                                         # check User grade
            x = Time(subject=instance.subject, description=instance.text, appendix=instance.code,
                     start_time=instance.start, end_time=instance.close)
            x.author_id = request.user.id
            x.group_id = request.user.groups.values_list('id', flat=True).first()
            x.save()                                                                            #check User grade
            return redirect('sulbigram:sulbi_list')
        return self.render_to_response({'form': form})

class SulbiUpdateView(LoginRequiredMixin, UpdateView):
    model = Sulbi
    form_class = DateForm
    #fields = ['department', 'code', 'subject', 'action', 'cycle', 'start', 'close', 'text', 'file', 'remark']
    template_name = 'sulbigram/sulbi_update.html'

    def sulbi_update(self, request, pk):
        instance=Sulbi()
        field_author = 'author'
        field_file = 'file'
        obj = Sulbi.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        file_field = getattr(obj, field_file)

        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author = author_field
        form.instance.file = file_field
        if form.is_valid():
            form.save()                                                                         # check User grade
            #Sulbi.objects.filter(id=pk).delete()
            return redirect('sulbigram:sulbi_list')
        return render(request, 'sulbigram/sulbi_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    group_id = request.user.groups.values_list('id', flat=True).first()                    #for group_name, replace 'id' with 'name'
    files = Sulbi.objects.filter(Q(author_id=request.user.id) & Q(group_id=group_id))
    html_string = render_to_string('sulbigram/pdf_list.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=sulbi_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = Sulbi.objects.filter(id=pk)                                                     # Model data
    html_string = render_to_string('sulbigram/pdf_detail.html', {'files': files})           # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=sulbi_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    group_name = request.user.groups.values_list('name', flat=True).first()
    file_filter = Ssulbi.objects.filter(Q(author=request.user.username) & Q(group=group_name))
    html_string = render_to_string('sulbigram/pdf_search.html', {'filter': file_filter})    # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=sulbi_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response
