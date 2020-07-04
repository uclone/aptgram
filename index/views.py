from django.shortcuts import render, redirect

def index_view(request):
    #return redirect('index:index')
    return render(request, 'index/index.html')

def index_mobile_view(request):
    #return redirect('index:mobile')
    return render(request, 'index/mobile.html')


