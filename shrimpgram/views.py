from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy, reverse
from .models import Shrimp, Sshrimp
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from django.db.models import Q
from .filters import SearchFilter
from .forms import RegistForm, MeterForm, ControlForm
from django.contrib.auth.models import User, Group
import xlwt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from time import mktime, strptime


@method_decorator(csrf_exempt, name='dispatch')
class IndexView(View):
    def post(self, request):
        #instance = Shrimp()
        #form = MeterForm(request.POST, instance=instance)
        #Iserial = form.instance.serial
        Iserial = request.POST['serial']
        form = Shrimp(serial = request.POST['serial'],
                      temp = request.POST['temp'],
                      ph = request.POST['ph'],
                      alkali = request.POST['alkali'],
                      salt = request.POST['salt'],
                      do = request.POST['do'],
                      nh4 = request.POST['nh4'],
                      turbid = request.POST['turbid'],)

        obj = Shrimp.objects.filter(serial=Iserial).last()
        group_field = getattr(obj, 'group')
        author_field = getattr(obj, 'author')
        location_field = getattr(obj, 'location')

        form.group = group_field
        form.author = author_field
        form.location = location_field
        form.serial = Iserial

        form.save()
        return HttpResponse(status=200)

    def get(self, request):
        Iserial = request.GET['serial']
        form = Shrimp(serial = Iserial,
                      temp = request.GET['temp'],
                      ph = request.GET['ph'],
                      alkali = request.GET['alkali'],
                      salt = request.GET['salt'],
                      do = request.GET['do'],
                      nh4 = request.GET['nh4'],
                      turbid = request.GET['turbid'],)

        obj = Shrimp.objects.filter(serial=Iserial).last()
        group_field = getattr(obj, 'group')
        author_field = getattr(obj, 'author')
        location_field = getattr(obj, 'location')

        form.group = group_field
        form.author = author_field
        form.location = location_field
        form.serial = Iserial

        form.save()
        return HttpResponse(status=200)

@login_required
def shrimp_list(request):
    pagefiles = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치'))
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
    return render(request, 'shrimpgram/shrimp_list.html', {'files':files})

@login_required
def control_list(request):
    pagefiles = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='조작장치'))
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
    return render(request, 'shrimpgram/control_list.html', {'files':files})

@login_required
def shrimp_search(request):
    file_list = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치'))
    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    xid = request.user.id
    Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).delete()
    for a in x:
        b = Sshrimp(id=a.id, author=a.author.username, group=xid, location=a.location, subject=a.subject, serial=a.serial,
                    temp=a.temp, ph=a.ph, alkali=a.alkali, salt=a.salt, do=a.do, nh4=a.nh4, no2=a.no2, turbid=a.turbid,
                    security=a.security, naoh=a.naoh, dang=a.dang, blower=a.blower,  boiler=a.boiler, remark=a.remark,
                    created=a.created, date=a.date, xdate=a.xdate)
        b.save()
    return render(request, 'shrimpgram/shrimp_search.html', {'filter': file_filter})

@login_required
def control_search(request):
    file_list = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='조작장치'))
    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='조작장치')).delete()
    for a in x:
        b = Sshrimp(id=a.id, author=a.author.username, group=a.group.name, location=a.location, subject=a.subject, serial=a.serial,
                    temp=a.temp, ph=a.ph, alkali=a.alkali, salt=a.salt, do=a.do, nh4=a.nh4, no2=a.no2, turbid=a.turbid,
                    security=a.security, naoh=a.naoh, dang=a.dang, blower=a.blower,  boiler=a.boiler, remark=a.remark, created=a.created)
        b.save()
    return render(request, 'shrimpgram/control_search.html', {'filter': file_filter})

class ShrimpDeleteView(LoginRequiredMixin, DeleteView):
    model = Shrimp
    success_url = reverse_lazy('shrimpgram:shrimp_list')
    template_name = 'shrimpgram/shrimp_delete.html'

class ShrimpUploadView(LoginRequiredMixin, CreateView):
    model = Shrimp
    form_class = RegistForm
    template_name = 'shrimpgram/shrimp_upload.html'

    def post(self, request):
        instance = Shrimp()
        form = RegistForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()                                                                         #check User grade
            return redirect('shrimpgram:shrimp_list')
        return self.render_to_response({'form': form})

class ControlUploadView(LoginRequiredMixin, CreateView):
    model = Shrimp
    form_class = ControlForm
    template_name = 'shrimpgram/control_upload.html'

    def post(self, request):
        instance = Shrimp()
        form = ControlForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        form.instance.serial = 'control'
        if form.is_valid():
            form.save()                                                                         #check User grade
            return redirect('shrimpgram:control_list')
        return self.render_to_response({'form': form})

class ShrimpUpdateView(LoginRequiredMixin, UpdateView):
    model = Shrimp
    form_class = MeterForm
    template_name = 'shrimpgram/shrimp_update.html'

    def shrimp_update(self, request, pk):
        instance = Shrimp()
        form = MeterForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()                                                                         # check User grade
            #Shrimp.objects.filter(id=pk).delete()
            return redirect('shrimpgram:shrimp_list')
        return render(request, 'shrimpgram/shrimp_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    files = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치'))
    html_string = render_to_string('shrimpgram/pdf_list.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=shrimp_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def control_pdf(request):
    files = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='조작장치'))
    html_string = render_to_string('shrimpgram/pdf_list_control.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=control_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    files_filter = Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='측정장치'))
    html_string = render_to_string('shrimpgram/pdf_search.html', {'filter': files_filter})                  # Rendered
    response = HttpResponse(content_type='application/pdf;')                                                # Creating http response
    response['Content-Disposition'] = 'filename=shrimp_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def control_search_pdf(request):
    files_filter = Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='조작장치'))
    html_string = render_to_string('shrimpgram/pdf_search_control.html', {'filter': files_filter})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                                                # Creating http response
    response['Content-Disposition'] = 'filename=control_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_xls(request):
    obj = Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).first()
    #author_name = getattr(obj, 'author')
    # Exel format
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=shrimp_search_{}.xls'.format(id)        #(author_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('측정자료')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['호지', '장치번호', '온도', 'ph', '알칼리도', '염도', '용존산소', '암모니아', '아질산', '탁도', '보안',]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).values_list('location', 'serial',
                                            'temp', 'ph', 'alkali', 'salt', 'do', 'nh4', 'no2', 'turbid', 'security')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

class ShrimpAPIView(LoginRequiredMixin, APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, idd):
        files = Sshrimp.objects.filter(Q(group=idd) & Q(subject='측정장치')).order_by('date')
        temp_list = []
        ph_list = []
        alkali_list = []
        salt_list = []
        do_list = []
        nh4_list = []
        no2_list = []
        turbid_list = []

        for file in files:
            org_date = str(file.date)
            new_date = org_date[:19]
            time_tuple = strptime(new_date, '%Y-%m-%d %H:%M:%S')
            utc_now = mktime(time_tuple) * 1000
            temp_list.append([utc_now, file.temp])
            ph_list.append([utc_now, file.ph])
            alkali_list.append([utc_now, file.alkali])
            salt_list.append([utc_now, file.salt])
            do_list.append([utc_now, file.do])
            nh4_list.append([utc_now, file.nh4])
            no2_list.append([utc_now, file.no2])
            turbid_list.append([utc_now, file.turbid])

        data = {
            'temp': temp_list,
            'ph': ph_list,
            'alkali': alkali_list,
            'salt': salt_list,
            'do': do_list,
            'nh4': nh4_list,
            'no2': no2_list,
            'turbid': turbid_list,
        }
        return Response(data)

class ChartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).first()
        return render(request, 'shrimpgram/shrimp_chart.html', {'form': form})

