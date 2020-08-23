from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import DeleteView
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar
from .forms import TimeForm

def index(request):
    return HttpResponse('hello')

#class CalendarView(generic.ListView):                      #Original
class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Time
    template_name = 'timegram/schedule.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        group_id = self.request.user.groups.values_list('id', flat=True).first()		#lbc inserted a new line
        html_cal = cal.formatmonth(group_id, withyear=True)                             #lbc inserted 'group_id',
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required
def event(request, event_id=None):
    instance = Time()
    if event_id:
        instance = get_object_or_404(Time, pk=event_id)
    else:
        instance = Time()

    form = TimeForm(request.POST or None, instance=instance)
#leebc ----
    form.instance.author_id = request.user.id
    form.instance.group_id = request.user.groups.values_list('id', flat=True).first()
#leebc ----
    if request.POST and form.is_valid():
        if instance.action=='일정 삭제':                       #leebc
            instance.delete()                           #leebc
        else:
            form.save()
        return HttpResponseRedirect(reverse('timegram:schedule'))
    return render(request, 'timegram/event.html', {'form': form})


