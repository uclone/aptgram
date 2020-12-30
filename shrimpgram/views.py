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
from .forms import RegistForm, ShrimpForm, ControlForm
from django.contrib.auth.models import User, Group
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
class IndexView(View):
    def post(self, request):
        Iserial = request.POST['serial']
        obj = Shrimp.objects.filter(Q(author_id=Iserial) & Q(remark='Register')).first()
        group_field = getattr(obj, 'group')
        author_field = getattr(obj, 'author')
        location_field = obj.location               #getattr(obj, 'location')
        form = Shrimp(serial = Iserial,
                      temp = request.POST['temp'],
                      ph = request.POST['ph'],
                      alkali = request.POST['alkali'],
                      salt = request.POST['salt'],
                      do = request.POST['do'],
                      nh4=request.POST['nh4'],
                      no2=request.POST['no2'],
                      turbid=request.POST['turbid'],
                      naoh=request.POST['naoh'],
                      dang=request.POST['dang'],)
        form.group = group_field
        form.author = author_field
        form.location = location_field
        form.save()                                 ################################
        form.date = form.created
        form.save()
        return HttpResponse(status=200)

    def get(self, request):
        Iserial = request.GET['serial']
        obj = Shrimp.objects.filter(Q(author_id=Iserial) & Q(remark='Register')).first()
        group_field = getattr(obj, 'group')
        author_field = getattr(obj, 'author')
        location_field = obj.location               #getattr(obj, 'location')
        form = Shrimp(serial = Iserial,
                      temp = request.GET['temp'],
                      ph = request.GET['ph'],
                      alkali = request.GET['alkali'],
                      salt = request.GET['salt'],
                      do = request.GET['do'],
                      nh4 = request.GET['nh4'],
                      no2 = request.GET['no2'],
                      turbid = request.GET['turbid'],
                      naoh = request.GET['naoh'],
                      dang = request.GET['dang'],)
        form.group = group_field
        form.author = author_field
        form.location = location_field
        form.save()                                 #######################################3
        form.date = form.created
        form.save()
        return HttpResponse(status=200)

@login_required
def shrimp_list(request):
    pagefiles = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치') & ~Q(remark='Register'))
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
def instrument_list(request):
    files = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(remark='Register'))
    return render(request, 'shrimpgram/instrument_list.html', {'files':files})

@login_required
def shrimp_search(request):
    file_list = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치')) # & ~Q(gasalarm='Register'))
    file_filter = SearchFilter(request.GET, queryset=file_list)
    # - Save in the other Table
    x = file_filter.qs
    xid = request.user.id
    Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).delete()
    for a in x:
        b = Sshrimp(id=a.id, author=a.author.username, group=xid, location=a.location, subject=a.subject, serial=a.serial,
                    temp=a.temp, ph=a.ph, alkali=a.alkali, salt=a.salt, do=a.do, nh4=a.nh4, no2=a.no2, turbid=a.turbid,
                    security=a.security, naoh=a.naoh, dang=a.dang, blower=a.blower,  boiler=a.boiler, remark=a.remark,
                    created=a.created, date=a.date,)
        b.save()
    return render(request, 'shrimpgram/shrimp_search.html', {'filter': file_filter})

def data_delete(request, pk):
    obj = Shrimp.objects.filter(id=pk).first()
    obj.delete
    files = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치') & ~Q(gasalarm='Register'))
    return render(request, 'shrimpgram/shrimp_list.html', {'files': files})

class ShrimpUploadView(LoginRequiredMixin, CreateView):
    model = Shrimp
    form_class = RegistForm
    template_name = 'shrimpgram/shrimp_upload.html'

    def post(self, request):
        mkey = request.POST['mk']
        instance = Shrimp()
        form = RegistForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save(commit=False)
            form.instance.mk = mkey
            form.instance.gasalarm = 'Register'
            form.save()
            # -------- for App -----------
            url = "http://www.smarteolife.com/push/register.php"
            data_dict = {
                "CMD": "COMMAND_REG",
                "TOKEN_TYP": "sec",
                "TOKEN_SER": request.POST['serial'],
                "TOKEN_PSW": mkey,                                      # request.POST['password'],
                "TOKEN_USR": request.user.username,                     # request.POST['username'],
                "TOKEN_TEL": request.user.last_name,                    # request.POST['last_name'],
                "TOKEN_EML": request.user.email,                        # request.POST['email'],
                "TOKEN_TLK": " ",
            }
            requests.get(url, params=data_dict)                         # response = requests.get(url, params=data_dict)
            # --------------------------
            return redirect('shrimpgram:shrimp_list')
        return self.render_to_response({'form': form})

class ControlUploadView(LoginRequiredMixin, CreateView):        # 직접 기록하는 경우
    model = Shrimp
    form_class = ControlForm
    template_name = 'shrimpgram/control_upload.html'

    def post(self, request):
        instance = Shrimp()
        form = ControlForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        location_field = form.instance.location
        if form.is_valid():
            form.save(commit=False)
            form.instance.subject = '직접기록'
            form.save()
            return redirect('shrimpgram:shrimp_list')
        return self.render_to_response({'form': form})

class ControlUpdateView(LoginRequiredMixin, UpdateView):
    model = Shrimp
    form_class = ControlForm
    template_name = 'shrimpgram/control_update.html'

def instrument_delete(request, pk):
    obj = Shrimp.objects.filter(id=pk).first()
    #pretype = obj.subject
    mserial = obj.serial
    mkey = obj.mk
    # -------- for App -----------
    type = "sec"
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
    obj.delete()
    files = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(remark='Regist'))
    return render(request, 'shrimpgram/shrimp_list.html', {'files': files})

#for weasyprint
def generate_pdf(request):
    files = Shrimp.objects.filter(Q(author_id=request.user.id) & Q(subject='측정장치'))
    html_string = render_to_string('shrimpgram/pdf_list.html', {'files': files})                        # Rendered
    response = HttpResponse(content_type='application/pdf;')                                            # Creating http response
    response['Content-Disposition'] = 'filename=shrimp_list_{}.pdf'.format(request.user)
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
    columns = ['호지', '장치번호', '온도(*C)', 'ph', '알칼리도(ppm)', '염도(ppt)', '용존산소(ppm)', '암모니아(ppm)',
               '아질산(ppm)', '탁도(ppm)', '중화제(cc/min)', '당밀(l/min)']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).values_list('location', 'serial',
                                            'temp', 'ph', 'alkali', 'salt', 'do', 'nh4', 'no2', 'turbid', 'naoh', 'dang',)

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num==2 or col_num==3 or col_num==6:
                ws.write(row_num, col_num, row[col_num]/10, font_style)
            elif col_num==7 or col_num==8:
                ws.write(row_num, col_num, row[col_num]/1000, font_style)
            else:
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
        naoh_list = []
        dang_list = []

        for file in files:
            org_date = str(file.date)
            new_date = org_date[:19]
            time_tuple = strptime(new_date, '%Y-%m-%d %H:%M:%S')
            utc_now = (mktime(time_tuple) + 32400) * 1000
            temp_list.append([utc_now, file.temp/10])
            ph_list.append([utc_now, file.ph])
            alkali_list.append([utc_now, file.alkali])
            salt_list.append([utc_now, file.salt])
            do_list.append([utc_now, file.do])
            nh4_list.append([utc_now, file.nh4])
            no2_list.append([utc_now, file.no2])
            turbid_list.append([utc_now, file.turbid])
            naoh_list.append([utc_now, file.naoh])
            dang_list.append([utc_now, file.dang])

        data = {
            'temp': temp_list,
            'ph': ph_list,
            'alkali': alkali_list,
            'salt': salt_list,
            'do': do_list,
            'nh4': nh4_list,
            'no2': no2_list,
            'turbid': turbid_list,
            'naoh': naoh_list,
            'dang': dang_list,
        }
        return Response(data)

class ChartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = Sshrimp.objects.filter(Q(author=request.user.username) & Q(subject='측정장치')).first()
        return render(request, 'shrimpgram/shrimp_chart.html', {'form': form})

