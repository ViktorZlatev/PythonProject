from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request , "mychatapp/index.html" , context)

def detail(request , pk):
    context = {}
    return render(request , "mychatapp/detail.html" , context)
