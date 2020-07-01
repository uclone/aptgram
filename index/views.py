from django.shortcuts import render, redirect

def index_view(request):
    #return redirect('index:index.html')
    return render(request, 'index/index.html')

def index_mobile_view(request):
    #return redirect('index:index.html')
    return render(request, 'index/index_mobile.html')


