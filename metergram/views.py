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
from .forms import ControlForm, MeterForm, RegistForm, CloseForm
import xlwt
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View
from time import mktime, strptime


@method_decorator(csrf_exempt, name='dispatch')
class MeterDataView(View):
    def post(self, request):
        Iserial = request.POST['serial']
        obj = Meter.objects.filter(Q(serial=Iserial) & Q(gasalarm='Register')).first()
        group_field = getattr(obj, 'group')
        author_field = getattr(obj, 'author')
        location_field = obj.location
        form = Meter(subject='스마트계량기',
                     serial=Iserial,
                     monmtr=request.POST['monmtr'],
                     moncor=request.POST['moncor'],
                     amtmonmtr=request.POST['amtmonmtr'],
                     amtmoncor=request.POST['amtmoncor'],
                     accmtr=request.POST['accmtr'],
                     acccor=request.POST['acccor'],
                     gastmp=request.POST['gastmp'],
                     gasprs=request.POST['gasprs'],
                     gasalarm=request.POST['gasalarm'], )
        form.save(commit=False)
        form.group = group_field
        form.author = author_field
        form.location = location_field
        form.save()
        return HttpResponse(status=200)

    def get(self, request):
        Iserial = request.GET['serial']
        obj = Meter.objects.filter(Q(serial=Iserial) & Q(gasalarm='Register')).first()
        group_field = getattr(obj, 'group')
        author_field = getattr(obj, 'author')
        location_field = obj.location
        form = Meter(subject = '스마트계량기',
                      serial = Iserial,
                      monmtr = request.GET['monmtr'],
                      moncor = request.GET['moncor'],
                      amtmonmtr=request.GET['amtmonmtr'],
                      amtmoncor=request.GET['amtmoncor'],
                      accmtr=request.GET['accmtr'],
                      acccor=request.GET['acccor'],
                      gastmp = request.GET['gastmp'],
                      gasprs = request.GET['gasprs'],
                      gasalarm = request.GET['gasalarm'],)
        form.save(commit=False)
        form.group = group_field
        form.author = author_field
        form.location = location_field
        form.save()
        return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
class ValveDataView(View):
    def post(self, request):
        Iserial = request.POST['serial']
        obj = Meter.objects.filter(Q(serial=Iserial) & Q(gasalarm='Register')).first()
        group_field = getattr(obj, 'group')
        author_field = getattr(obj, 'author')
        location_field = obj.location
        form = Meter(subject = '스마트차단기',
                      serial = Iserial,
                      hometmp = request.POST['hometmp'],
                      homeprs = request.POST['homeprs'],
                      homealarm = request.POST['homealarm'],
                      valvestatus = request.POST['valvestatus'],
                      valveaction = request.POST['valveaction'],)
        form.save(commit=False)
        form.group = group_field
        form.author = author_field
        form.location = location_field
        form.save()
        return HttpResponse(status=200)

    def get(self, request):
        Iserial = request.GET['serial']
        obj = Meter.objects.filter(Q(serial=Iserial) & Q(gasalarm='Register')).first()
        group_field = getattr(obj, 'group')
        author_field = getattr(obj, 'author')
        location_field = obj.location
        form = Meter(subject = '스마트차단기',
                      serial = Iserial,
                      hometmp = request.GET['hometmp'],
                      homeprs = request.GET['homeprs'],
                      homealarm = request.GET['homealarm'],
                      valvestatus=request.POST['valvestatus'],
                      valveaction=request.POST['valveaction'], )
        form.save(commit=False)
        form.group = group_field
        form.author = author_field
        form.location = location_field
        form.save()
        return HttpResponse(status=200)

class ValveCloseView(LoginRequiredMixin, CreateView):        #스마트차단기 작동
    model = Meter
    form_class = CloseForm
    template_name = 'metergram/valve_close.html'

    def post(self, request):
        obj = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트차단기')).first()
        location_field = obj.location
        serial_field = obj.serial
        mk_field = obj.mk
        instance = Meter()
        form = CloseForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save(commit=False)
            form.instance.location = location_field
            form.instance.serial = serial_field
            form.instance.mk = mk_field
            form.instance.subject = '스마트차단기'
            form.instance.valveaction = '가스밸브 차단작동'
            form.save()
            # -------- for App -----------
            url = "http://www.smarteolife.com/push/register.php"
            data_dict = {
                "CMD": "COMMAND_TLK",
                "TOKEN_TYP": "gop",
                "TOKEN_SER": serial_field,
                "TOKEN_PSW": mk_field,                          # request.POST['password'],
                "TOKEN_USR": request.user.username,             # request.POST['username'],
                "TOKEN_TEL": request.user.last_name,            # request.POST['last_name'],
                "TOKEN_EML": request.user.email,                # request.POST['email'],
                "TOKEN_TLK": "afrtsclose",
            }
            requests.get(url, params=data_dict)                 # response = requests.get(url, params=data_dict)
            # --------------------------
            return redirect('metergram:control_list')
        return self.render_to_response({'form': form})

@login_required
def meter_list(request):
    pagefiles = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트계량기'))
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
    pagefiles = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트차단기'))
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
    file_list = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트계량기'))
    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    xid = request.user.id
    Smeter.objects.filter(Q(author=request.user.username) & Q(subject='스마트계량기')).delete()
    for a in x:
        b = Smeter(id=a.id, author=a.author.username, group=xid, location=a.location, subject=a.subject, serial=a.serial,
                   monmtr=a.monmtr, moncor=a.moncor, amtmonmtr=a.amtmonmtr, amtmoncor=a.amtmoncor, accmtr=a.accmtr,
                   acccor=a.acccor, gastmp=a.gastmp, gasprs=a.gasprs, gasalarm=a.gasalarm, created=a.created, date=a.date)
        b.save()
    return render(request, 'metergram/meter_search.html', {'filter': file_filter})

@login_required
def control_search(request):
    file_list = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트차단기'))
    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    xid = request.user.id
    Smeter.objects.filter(Q(author=request.user.username) & Q(subject='스마트차단기')).delete()
    for a in x:
        b = Smeter(id=a.id, author=a.author.username, group=xid, location=a.location, subject=a.subject, serial=a.serial,
                   hometmp=a.hometmp, homehumid=a.homehumid, homealarm=a.homealarm, valvestatus=a.valvestatus,
                   valveaction=a.valveaction, created=a.created, date=a.date)
        b.save()
    return render(request, 'metergram/control_search.html', {'filter': file_filter})

def meter_delete(request, pk):
    obj = Meter.objects.filter(id=pk).first()
    pretype = obj.subject
    mserial = obj.serial
    mkey = obj.mk
    # -------- for App -----------
    if "차단기" in pretype:
        type = "gop"
    else:
        type = "gvc"
    url = "http://www.smarteolife.com/push/register.php"
    data_dict = {
        "CMD": "COMMAND_DEL",
        "TOKEN_TYP": type,
        "TOKEN_SER": mserial,
        "TOKEN_PSW": mkey,
        "TOKEN_USR": request.user.username,                     # request.POST['username'],
        "TOKEN_TEL": request.user.last_name,                    # request.POST['last_name'],
        "TOKEN_EML": request.user.email,                        # request.POST['email'],
        "TOKEN_TLK": " ",
    }
    requests.get(url, params=data_dict)                         # response = requests.get(url, params=data_dict)
    # --------------------------
    Meter.objects.filter(id=pk).delete()
    if type=="gvc":
        files = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트계량기'))
        return render(request, 'metergram/meter_list.html', {'files': files})
    elif type=="gop":
        files = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트차단기'))
        return render(request, 'metergram/control_list.html', {'files': files})

class MeterUpdateView(LoginRequiredMixin, UpdateView):
    model = Meter
    form_class = MeterForm
    template_name = 'metergram/meter_update.html'

class MeterUploadView(LoginRequiredMixin, CreateView):              #스마트계량기 등록
    model = Meter
    form_class = RegistForm
    template_name = 'metergram/meter_upload.html'

    def post(self, request):
        mkey = request.POST['mk']
        instance = Meter()
        form = RegistForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save(commit=False)
            form.instance.mk = mkey
            form.instance.gasalarm ='Register'
            form.save()
            #-------- for App -----------
            typ = request.POST['subject']
            if "차단기" in typ:
                type = "gop"
            else:
                type = "gvc"
            url = "http://www.smarteolife.com/push/register.php"
            data_dict = {
                "CMD": "COMMAND_REG",
                "TOKEN_TYP": type,
                "TOKEN_SER": request.POST['serial'],
                "TOKEN_PSW": mkey,
                "TOKEN_USR": request.user.username,                     # request.POST['username'],
                "TOKEN_TEL": request.user.last_name,                    # request.POST['last_name'],
                "TOKEN_EML": request.user.email,                        # request.POST['email'],
                "TOKEN_TLK": " ",
            }
            requests.get(url, params=data_dict)                         # response = requests.get(url, params=data_dict)
            #--------------------------
            return redirect('metergram:meter_list')
        return self.render_to_response({'form': form})

#for weasyprint
def generate_pdf(request):
    files = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트계량기'))
    html_string = render_to_string('metergram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=meter_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def control_pdf(request):
    files = Meter.objects.filter(Q(author_id=request.user.id) & Q(subject='스마트차단기'))
    html_string = render_to_string('metergram/pdf_list_control.html', {'files': files})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=control_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    files_filter = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='스마트계량기'))
    html_string = render_to_string('metergram/pdf_search.html', {'filter': files_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=meter_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def control_search_pdf(request):
    files_filter = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='스마트차단기'))
    html_string = render_to_string('metergram/pdf_search_control.html', {'filter': files_filter})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                                                # Creating http response
    response['Content-Disposition'] = 'filename=control_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_xls(request):
    obj = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='스마트계량기')).first()
    #author_name = getattr(obj, 'author')
    # Exel format
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=meter_search_{}.xls'.format(id)        #(author_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('계량자료')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['동/호', '장치번호', '계량사용량', '보정사용량', '누적계량값', '누적보정값', '가스온도(*C)', '가스압력(kPa)',
               '가스알림', '시간',]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='스마트계량기')).values_list('location',
                'serial', 'monmtr', 'moncor', 'accmtr', 'acccor', 'gastmp', 'gasprs', 'gasalarm', 'created')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num>1 and col_num<6:
                ws.write(row_num, col_num, row[col_num]/100, font_style)
            elif col_num>5 and col_num<7:
                ws.write(row_num, col_num, row[col_num]/10, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

class MeterAPIView(LoginRequiredMixin, APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, idd):
        files = Smeter.objects.filter(Q(group=idd) & Q(subject='스마트계량기')).order_by('created')
        monmtr_list = []
        moncor_list = []
        accmtr_list = []
        acccor_list = []
        gastmp_list = []
        gasprs_list = []

        for file in files:
            org_date = str(file.created)
            new_date = org_date[:19]
            time_tuple = strptime(new_date, '%Y-%m-%d %H:%M:%S')
            utc_now = (mktime(time_tuple) + 32400) * 1000
            monmtr_list.append([utc_now, file.monmtr/100])
            moncor_list.append([utc_now, file.moncor/100])
            accmtr_list.append([utc_now, file.accmtr/10000])
            acccor_list.append([utc_now, file.acccor/10000])
            gastmp_list.append([utc_now, file.gastmp/10])
            gasprs_list.append([utc_now, file.gasprs/10])

        data = {
            'monmtr': monmtr_list,
            'moncor': moncor_list,
            'accmtr': accmtr_list,
            'acccor': acccor_list,
            'gastmp': gastmp_list,
            'gasprs': gasprs_list,
        }
        return Response(data)

class MeterChartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = Smeter.objects.filter(Q(author=request.user.username) & Q(subject='스마트계량기')).first()
        return render(request, 'metergram/meter_chart.html', {'form': form})


