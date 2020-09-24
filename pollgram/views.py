from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy, reverse
from .models import Poll, Choice, Spoll
from jumingram.models import Jumin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import weasyprint
from .filters import SearchFilter
from .forms import PollForm, ChoiceForm
from django.utils import timezone
from datetime import datetime, timedelta, date
import operator


@login_required
def poll_list(request):
    group_id = request.user.groups.values_list('id', flat=True).first()
    pagefiles = Poll.objects.filter(group_id=group_id)
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
    return render(request, 'pollgram/poll_list.html', {'files':files})

@login_required
def poll_search(request):
    group_id = request.user.groups.values_list('id', flat=True).first()
    file_list = Poll.objects.filter(group_id=group_id)
    # filtering routine
    file_filter = SearchFilter(request.GET, queryset=file_list)
    x = file_filter.qs
    Spoll.objects.all().delete()
    for a in x:
        b = Spoll(id=a.id, subject=a.subject, pub_date=a.pub_date, open_date=a.open_date,
                  close_date=a.close_date, remark=a.remark, created=a.created, updated=a.updated)
        b.save()
    return render(request, 'pollgram/poll_search.html', {'filter': file_filter})

def poll_upload(request):
    if request.method == "POST":
        pform = PollForm(request.POST, instance=Poll())
        pform.instance.author_id = request.user.id
        pform.instance.group_id = request.user.groups.values_list('id', flat=True).first()
        cform = [ChoiceForm(request.POST, prefix=str(x), instance=Choice()) for x in range(0,7)]
        if pform.is_valid() and all([cf.is_valid() for cf in cform]):
            new_poll = pform.save()
            for cf in cform:
                new_choice = cf.save(commit=False)
                new_choice.poll = new_poll
                new_choice.save()
            return redirect('pollgram:poll_list')
    else:
        pform = PollForm(instance=Poll())
        cform = [ChoiceForm(prefix=str(x), instance=Choice()) for x in range(0,7)]
    return render(request, 'pollgram/poll_upload.html', {'pform': pform, 'cform': cform})

def poll_detail(request, pk):
    pform = get_object_or_404(Poll, id=pk)
    cform = Choice.objects.filter(poll=pform)
    return render(request, 'pollgram/poll_detail.html', {'pform': pform, 'cform': cform})

class PollDeleteView(LoginRequiredMixin, DeleteView):
    model = Poll
    success_url = reverse_lazy('pollgram:poll_list')
    template_name = 'pollgram/poll_delete.html'

def poll_update(request, pk):
    quest = get_object_or_404(Poll, id=pk)
    pform = PollForm(request.POST, instance=quest)
    pform.instance.author_id = request.user.id
    pform.instance.group_id = request.user.groups.values_list('id', flat=True).first()
    subject_field = getattr(quest, 'subject')
    request.POST._mutable = True
    request.POST['subject'] = subject_field
    cform = [ChoiceForm(request.POST, prefix=str(ch.id), instance=ch) for ch in quest.choice_set.all()]
    if pform.is_valid() and all([cf.is_valid() for cf in cform]):
        new_poll = pform.save()
        for cf in cform:
            new_choice = cf.save(commit=False)
            new_choice.question = new_poll
            new_choice.save()
        return redirect('pollgram:poll_list')
    return render(request, 'pollgram/poll_update.html', {'pform': pform, 'cform': cform})

def poll_vote(request, pk):
    jumin = Jumin.objects.filter(author_id=request.user.id).first()
    if jumin.ticket < 1:
        pform = get_object_or_404(Poll, id=pk)
        cform = Choice.objects.filter(poll=pform)
        return render(request, 'pollgram/poll_vote.html', {'pform': pform, 'cform': cform, 'error_message': "투표권이 없습니다."})
    # voting routine --------
    try:
        pform = get_object_or_404(Poll, id=pk)
        selected = pform.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        pform = get_object_or_404(Poll, id=pk)
        cform = Choice.objects.filter(poll=pform)
        return render (request, 'pollgram/poll_vote.html', {'pform': pform, 'cform': cform, 'error_message': "투표를 기권하십니까?"})
    else:
        selected.votes += 1
        selected.save()
        jumin.ticket -= 1                                   #투표권
        jumin.save()                                        #투표권
        pform = get_object_or_404(Poll, id=pk)
        cform = Choice.objects.filter(poll=pform)
        return render(request, 'pollgram/poll_vote.html', {'pform': pform, 'cform': cform, 'error_message': "투표를 완료하셨습니다.."})

def all(items):
    from functools import reduce
    import operator
    return reduce(operator.and_, [bool(item) for item in items])

def generate_pdf(request):
    files = Poll.objects.filter(author_id=request.user.id)
    html_string = render_to_string('pollgram/pdf_list.html', {'files': files})              # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=poll_list_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response, stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def search_pdf(request):
    file_filter = Spoll.objects.all()
    html_string = render_to_string('pollgram/pdf_search.html', {'filter': file_filter})     # Rendered
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=poll_search_{}.pdf'.format(request.user)
    weasyprint.HTML(string=html_string).write_pdf(response, stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response

def detail_pdf(request, pk):
    pfiles = get_object_or_404(Poll, id=pk)
    cfiles = Choice.objects.filter(poll=pfiles)
    html_string = render_to_string('pollgram/pdf_detail.html', {'pfiles': pfiles, 'cfiles': cfiles})
    response = HttpResponse(content_type='application/pdf;')                                # Creating http response
    response['Content-Disposition'] = 'filename=poll_detail_{}_{}.pdf'.format(request.user, pk)
    weasyprint.HTML(string=html_string).write_pdf(response, stylesheets=[weasyprint.CSS('static/css/pdf.css')])
    return response


#class PollUpdateView(LoginRequiredMixin, UpdateView):
#    model = Poll, Choice
#    form_class = PollForm, ChoiceForm
#    template_name = 'pollgram/poll_update.html'
#    def poll_update(self, request, pk):
#        quest = get_object_or_404(Poll, id=pk)
#        pform = PollForm(request.POST, instance=quest)
#        cform = [ChoiceForm(request.POST, prefix=str(ch.id), instance=ch) for ch in quest.choice_set.all()]
#        if pform.is_valid() and all([cf.is_valid() for cf in cform]):
#            new_poll = pform.save()
#            for cf in cform:
#                new_choice = cf.save(commit=False)
#                new_choice.question = new_poll
#                new_choice.save()
#            return redirect('pollgram:poll_list')
#        return render(request, 'pollgram/poll_update.html', {'pform': pform, 'cform': cform})

#def poll_result(request, pk):
#    form = get_object_or_404(Poll, id=pk)
#    return render(request, 'pollgram/poll_result', {'form':form})
