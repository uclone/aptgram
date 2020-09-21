from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy, reverse
from .models import Equip, Sequip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import DateForm
from django.contrib.auth.models import User, Group

@login_required
def equip_list(request):
    #try:
    #    request_user = request.user
    #    data = Equip.objects.filter(author_id=request_user.id).first()
    #    pagefiles = Equip.objects.filter(group_id=data.group_id)
    #except:
    #    pagefiles = Equip.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name or '2급' in request.user.last_name:
            pagefiles = Equip.objects.filter(group_id=group_id)
        else:
            pagefiles_1 = Equip.objects.filter(group_id=group_id)
            pagefiles = pagefiles_1.objects.filter(department__icontains=user_dept)
    except:
        pagefiles = Equip.objects.filter(group_id=1)

# - pagination - start
    page = request.GET.get('page', 1)
    paginator = Paginator(pagefiles, 10)
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
    #try:
    #    request_user = request.user
    #    data = Equip.objects.filter(author_id=request_user.id).first()
    #    file_list = Equip.objects.filter(group_id=data.group_id)
    #except:
    #    file_list = Equip.objects.filter(group_id=1)

    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name or '2급' in request.user.last_name:
            file_list = Equip.objects.filter(group_id=group_id)
        else:
            file_list_1 = Equip.objects.filter(group_id=group_id)
            file_list = file_list_1.objects.filter(department__icontains=user_dept)
    except:
        file_list = Equip.objects.filter(group_id=1)                                #.order_by('author')

    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    Sequip.objects.all().delete()
    for a in x:
        b = Sequip(id=a.id, code=a.code, subject=a.subject, location=a.location, department=a.department,
                   manager_1=a.manager_1, manager_2=a.manager_2, spec=a.spec, date=a.date, remark=a.remark, file=a.file)
        b.save()
    return render(request, 'equipgram/equip_search.html', {'filter': file_filter})

class EquipDeleteView(LoginRequiredMixin, DeleteView):
    model = Equip
    success_url = reverse_lazy('equipgram:equip_list')
    template_name = 'equipgram/equip_delete.html'

class EquipUploadView(LoginRequiredMixin, CreateView):
    model = Equip
    form_class = DateForm
    template_name = 'equipgram/equip_upload.html'
    #success_url = reverse_lazy('equipgram:equip_list)

    def post(self, request):
        instance = Equip()
        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()

        if form.is_valid():
            user_dept = request.user.last_name[0:2]                                                 # check User grade
            if '1급' in request.user.last_name:                                                      #check User grade
                form.save()                                                                         #check User grade
            elif '2급' in request.user.last_name and user_dept in instance.department:               # check User grade
                form.instance.remark = ' '
                form.save()                                                                         # check User grade
            return redirect('equipgram:equip_list')
        return self.render_to_response({'form': form})

class EquipUpdateView(LoginRequiredMixin, UpdateView):
    model = Equip
    form_class = DateForm
    template_name = 'equipgram/equip_update.html'

    def equip_update(self, request, pk):
        instance = Equip()
        field_author = 'author'
        field_file = 'file'
        obj = Equip.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        file_field = getattr(obj, field_file)
        form = DateForm(request.POST, request.FILES, instance=instance)
        form.instance.author = author_field
        form.instance.file = file_field

        if form.is_valid():
            user_dept = request.user.last_name[0:2]  # check User grade
            if '1급' in request.user.last_name:                                                      #check User grade
                form.save()                                                                         #check User grade
            elif '2급' in request.user.last_name and user_dept in instance.department:               # check User grade
                form.instance.remark = ' '
                form.save()                                                                         # check User grade
            Equip.objects.filter(id=pk).delete()
            return redirect('equipgram:equip_list')
        return render(request, 'equipgram/equip_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        user_dept = request.user.last_name[0:2]                                     #for user's department
        if '1급' in request.user.last_name or '2급' in request.user.last_name:
            files = Equip.objects.filter(group_id=group_id)
        else:
            files_1 = Equip.objects.filter(group_id=group_id)
            files = files_1.objects.filter(department__icontains=user_dept)
    except:
        files = Equip.objects.filter(group_id=1)                                    #.order_by('author')

    html_string = render_to_string('equipgram/pdf_list.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=equip_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = Equip.objects.filter(id=pk)                                        # Model data
    html_string = render_to_string('equipgram/pdf_detail.html', {'files': files})           # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=equip_detail_{}_{}.pdf'.format(request.user, pk)    #user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    files_filter = Sequip.objects.all()
    html_string = render_to_string('equipgram/pdf_search.html', {'filter': files_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=equip_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

