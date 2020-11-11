from django.shortcuts import render
from nameapp.models import KospiPredict
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import View

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NameForm, DateForm

from time import mktime, strptime

def name_list(request):
    files = KospiPredict.objects.all()
    return render(request, 'nameapp/name_list.html', {'files':files})

class NameUploadView(LoginRequiredMixin, CreateView):
    model = KospiPredict
    form_class = DateForm
    template_name = 'nameapp/name_upload.html'

    def post(self, request):
        form = DateForm(request.POST)
        form.instance.author_id = request.user.id
        form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        if form.is_valid():
            form.save()
            return redirect('nameapp:name_list')
        return self.render_to_response({'form': form})


class KospiPredictAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        stocks = KospiPredict.objects.all().order_by('date')
        close_list = []
        open_list = []
        for stock in stocks:
            time_tuple = strptime(str(stock.date), '%Y-%m-%d')
            utc_now = mktime(time_tuple) * 1000
            close_list.append([utc_now, stock.close])
            open_list.append([utc_now, stock.open])

        data = {
            'close': close_list,
            'open': open_list
        }

        return Response(data)

class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'nameapp/chart.html')