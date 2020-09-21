from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy, reverse
from .models import Susun, Ssusun
from timegram.models import Time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import SusunForm, DateForm
from timegram.forms import TimeForm
import xlwt

@login_required
def susun_list(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        pagefiles = Susun.objects.filter(group_id=group_id)
    except:
        pagefiles = Susun.objects.filter(group_id=1)
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
    return render(request, 'susungram/susun_list.html', {'files':files})

@login_required
def susun_search(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()
        file_list = Susun.objects.filter(group_id=group_id)
    except:
        file_list = Susun.objects.filter(group_id=1)

    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Ssusun.objects.all().delete()
    for a in x:
        b = Ssusun(id=a.id, category=a.category, subject=a.subject, treatment=a.treatment, method=a.method, cycle=a.cycle,
                   ratio=a.ratio, last=a.last, rule=a.rule, plan=a.plan, cost=a.cost, times=a.times, amount=a.amount)
        b.save()
    return render(request, 'susungram/susun_search.html', {'filter': file_filter})

class SusunDeleteView(LoginRequiredMixin, DeleteView):
    model = Susun
    success_url = reverse_lazy('susungram:susun_list')
    template_name = 'susungram/susun_delete.html'

class SusunUploadView(LoginRequiredMixin, CreateView):
    model = Susun
    form_class = DateForm
    template_name = 'susungram/susun_upload.html'

    def post(self, request):
        instance = Susun()
        form = DateForm(request.POST, instance=instance)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        form.instance.amount = form.instance.cost                                                 # calculating Amount
        form.instance.amount *= form.instance.times
        if form.is_valid():
            form.save()
            x = Time(subject=instance.subject, description=instance.treatment, appendix=instance.method,
                     start_time=instance.plan, end_time=instance.rule)
            x.author_id = request.user.id
            x.group_id = request.user.groups.values_list('id', flat=True).first()
            x.save()
            return redirect('susungram:susun_list')
        return self.render_to_response({'form': form})

class SusunUpdateView(LoginRequiredMixin, UpdateView):
    model = Susun
    form_class = DateForm
    template_name = 'susungram/susun_update.html'

    def susun_update(self, request, pk):
        field_author = 'author'
        field_file = 'file'
        obj = Susun.objects.filter(id=pk).first()
        author_field = getattr(obj, field_author)
        file_field = getattr(obj, field_file)

        form = DateForm(request.POST, request.FILES)
        form.instance.author = author_field
        form.instance.file = file_field
        if form.is_valid():
            form.save()
#            Susun.objects.filter(id=pk).delete()
            return redirect('susungram:susun_list')
        return render(request, 'susungram/susun_update.html', {'form': form})

#for weasyprint
def generate_pdf(request):
    try:
        group_id = request.user.groups.values_list('id', flat=True).first()         #for group_name, replace 'id' with 'name'
        files = Susun.objects.filter(group_id=group_id)                             #.order_by('author')
    except:
        files = Susun.objects.filter(group_id=1)                                    #.order_by('author')

    html_string = render_to_string('susungram/pdf_list.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=susun_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    files = Susun.objects.filter(id=pk)                                   # Model data
    html_string = render_to_string('susungram/pdf_detail.html', {'files': files})          # Rendered
    response = HttpResponse(content_type='application/pdf;')                            # Creating http response
    response['Content-Disposition'] = 'filename=susun_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Ssusun.objects.all()
    html_string = render_to_string('susungram/pdf_search.html', {'filter': file_filter})             # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=susun_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response,
                                           stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_xls(request):
    group_idd = request.user.groups.values_list('id', flat=True).first()
    field_group = 'group'
    obj = Susun.objects.filter(group_id=group_idd).first()
    group_name = getattr(obj, field_group)
    # Exel format
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=susun_search_{}.xls'.format(group_name)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('장기수선예정내역')
    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['대분류', '구분', '공사종별', '수선방법', '수선주기(년)', '수선율(%)',
                  '최종수선(년)', '법정예정(년)', '최종수정연', '수선예정금(원)', '예정회수', '총수선예정금']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Ssusun.objects.all().values_list('category', 'subject', 'treatment', 'method', 'cycle', 'ratio',
                  'last', 'rule', 'plan', 'cost', 'times', 'amount')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response