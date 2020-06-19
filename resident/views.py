from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from .models import Resident

# Create your views here.
class ResidentListView(ListView):
    model = Resident
    paginate_by = 6
    template_name = 'resident/resident_list.html'

class ResidentCreateView(CreateView):
    model = Resident
    fields = ['dong', 'ho', 'represent', 'family', 'phone', 'date', 'car', 'remark']
    success_url = reverse_lazy('resident:resident_list')
    template_name = 'resident/resident_create.html'

class ResidentUpdateView(UpdateView):
    model = Resident
    fields = ['dong', 'ho', 'represent', 'family', 'phone', 'date', 'car', 'remark']
    success_url = reverse_lazy('resident:resident_list')
    template_name = 'resident/resident_update.html'

class ResidentDeleteView(DeleteView):
    model = Resident
    success_url = reverse_lazy('resident:resident_list')

class ResidentDetailView(DetailView):
    model = Resident
    template_name = 'resident/resident_detail.html'




