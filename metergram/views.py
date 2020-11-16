from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from .models import Meter, Smeter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from django.db.models import Q
from .filters import SearchFilter
from .forms import ControlForm, MeterForm, RegistForm
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
        form = Meter(serial = request.POST['serial'],
                      mtr = request.POST['mtr'],
                      cor = request.POST['cor'],
                      elec = request.POST['elec'],
                      water = request.POST['water'],
                      temp = request.POST['temp'],
                      humidity= request.POST['humidity'],
                      usegas = request.POST['usegas'],
                      usewater = request.POST['usewater'],
                      alarm = request.POST['alarm'],)

        obj = Meter.objects.filter(serial=Iserial).last()
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
        form = Meter(serial = Iserial,
                     mtr=request.GET['mtr'],
                     cor=request.GET['cor'],
                     elec=request.GET['elec'],
                     water=request.GET['water'],
                     temp=request.GET['temp'],
                     humidity=request.GET['humidity'],
                     usegas=request.GET['usegas'],
                     usewater=request.GET['usewater'],
                     alarm=request.GET['alarm'], )

        obj = Meter.objects.filter(serial=Iserial).last()
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
def meter_list(request):
    pagefiles = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치'))
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
def control_list(request):
    pagefiles = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='조작장치'))
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
    return render(request, 'metergram/control_list.html', {'files':files})

@login_required
def meter_search(request):
    file_list = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치'))
    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    xid = request.user.id
    Smeter.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).delete()
    for a in x:
        b = Smeter(id=a.id, author=a.author.username, group=xid, location=a.location, subject=a.subject, serial=a.serial,
                   mtr=a.mtr, cor=a.cor, elec=a.elec, water=a.water, temp=a.temp, humidity=a.humidity, usegas=a.usegas,
                   usewater=a.usewater, alarm=a.alarm, actgas=a.actgas, actalarm=a.actalarm, remark=a.remark,
                   created=a.created, date=a.date)
        b.save()
    return render(request, 'metergram/meter_search.html', {'filter': file_filter})

@login_required
def control_search(request):
    file_list = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='조작장치'))
    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    Smeter.objects.filter(Q(author=request.user.username) & Q(subject='조작장치')).delete()
    for a in x:
        b = Smeter(id=a.id, author=a.author.username, group=a.group.name, location=a.location, subject=a.subject, serial=a.serial,
                   mtr=a.mtr, cor=a.cor, elec=a.elec, water=a.water, temp=a.temp, humidity=a.humidity, usegas=a.usegas,
                   usewater=a.usewater, alarm=a.alarm, actgas=a.actgas, actalarm=a.actalarm, remark=a.remark,
                   created=a.created, date=a.date)
        b.save()
    return render(request, 'metergram/control_search.html', {'filter': file_filter})

class MeterDeleteView(LoginRequiredMixin, DeleteView):
    model = Meter
    success_url = reverse_lazy('metergram:meter_list')
    template_name = 'metergram/meter_delete.html'

class MeterUploadView(LoginRequiredMixin, CreateView):
    model = Meter
    form_class = RegistForm
    template_name = 'metergram/meter_upload.html'

    def post(self, request):
        instance = Meter()
        form = RegistForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()
            return redirect('metergram:meter_list')
        return self.render_to_response({'form': form})

class ControlUploadView(LoginRequiredMixin, CreateView):
    model = Meter
    form_class = ControlForm
    template_name = 'metergram/control_upload.html'

    def post(self, request):
        instance = Meter()
        form = ControlForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()                                                                         #check User grade
            return redirect('metergram:control_list')
        return self.render_to_response({'form': form})

class MeterUpdateView(LoginRequiredMixin, UpdateView):
    model = Meter
    form_class = MeterForm
    template_name = 'metergram/meter_update.html'

    def meter_update(self, request, pk):
        instance = Meter()
        form = MeterForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()                                                                         # check User grade
            #Shrimp.objects.filter(id=pk).delete()
            return redirect('metergram:meter_list')
        return render(request, 'metergram/meter_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    files = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치'))
    html_string = render_to_string('metergram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=meter_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def control_pdf(request):
    files = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='조작장치'))
    html_string = render_to_string('metergram/pdf_list_control.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=control_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    files_filter = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='측정장치'))
    html_string = render_to_string('metergram/pdf_search.html', {'filter': files_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=meter_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def control_search_pdf(request):
    files_filter = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='조작장치'))
    html_string = render_to_string('metergram/pdf_search_control.html', {'filter': files_filter})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                                                # Creating http response
    response['Content-Disposition'] = 'filename=control_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_xls(request):
    obj = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).first()
    #author_name = getattr(obj, 'author')
    # Exel format
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=meter_search_{}.xls'.format(id)        #(author_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('측정자료')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['동/호', '장치번호', '계량값', '보정값', '전기미터', '수도미터', '온도(*C)', '습도(%)', '가스사용', '수도사용', '경보',]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).values_list('location', 'serial',
                                            'mtr', 'cor', 'elec', 'water', 'temp', 'humidity', 'usegas', 'usewater', 'alarm')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num>1 and col_num<6:
                ws.write(row_num, col_num, row[col_num]/100, font_style)
            elif col_num==6:
                ws.write(row_num, col_num, row[col_num]/10, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

class MeterAPIView(LoginRequiredMixin, APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, idd):
        files = Smeter.objects.filter(Q(group=idd) & Q(subject='측정장치')).order_by('date')
        mtr_list = []
        cor_list = []
        elec_list = []
        water_list = []
        temp_list = []
        humidity_list = []

        for file in files:
            org_date = str(file.date)
            new_date = org_date[:19]
            time_tuple = strptime(new_date, '%Y-%m-%d %H:%M:%S')
            utc_now = (mktime(time_tuple) + 32400) * 1000
            mtr_list.append([utc_now, file.mtr/100])
            cor_list.append([utc_now, file.cor/100])
            elec_list.append([utc_now, file.elec/100])
            water_list.append([utc_now, file.water/100])
            temp_list.append([utc_now, file.temp/10])
            humidity_list.append([utc_now, file.humidity])

        data = {
            'mtr': mtr_list,
            'cor': cor_list,
            'elec': elec_list,
            'water': water_list,
            'temp': temp_list,
            'humidity': humidity_list,
        }
        return Response(data)

class MeterChartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).first()
        return render(request, 'metergram/meter_chart.html', {'form': form})