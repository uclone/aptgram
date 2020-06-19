from django.shortcuts import render, redirect

def index_view(request):
    #return redirect('index:index.html')
    return render(request, 'index/index.html')


